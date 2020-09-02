"""
Main file for CVAT tracker utility.
"""


from argparse import ArgumentParser
from contextlib import ExitStack

from loguru import logger

from .api import Authenticator
from .cvat_dataset import CvatDataset
from .tracker import Tracker


def _make_parser() -> ArgumentParser:
    """
    Returns:
        The parser to use for parsing CLI arguments.
    """
    parser = ArgumentParser(
        prog="cvat_tracker",
        description="Program that uses tracking to propagate annotations from "
        "one frame to the next.",
    )

    parser.add_argument(
        "-u",
        "--username",
        required=True,
        help="The username to use for logging into CVAT.",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=True,
        help="The password to use for logging into CVAT.",
    )
    parser.add_argument(
        "--url",
        default="localhost:8080",
        help="The CVAT server to connect to.",
    )

    parser.add_argument(
        "-t",
        "--task-id",
        type=int,
        help="The numerical ID of the task to modify.",
    )
    parser.add_argument(
        "-f", "--frame", type=int, help="The frame to start tracking at."
    )

    parser.add_argument(
        "--show-result",
        action="store_true",
        help="Enables a debugging display that shows the transformed "
        "annotations.",
    )

    return parser


@logger.catch()
def main() -> None:
    parser = _make_parser()
    args = parser.parse_args()

    with ExitStack() as exit_stack:
        auth = exit_stack.enter_context(
            Authenticator.from_new_session(
                user=args.username, password=args.password, host=args.url
            )
        )
        provider = exit_stack.enter_context(
            CvatDataset.for_task(task_id=args.task_id, auth=auth)
        )

        # Update the annotations with tracking.
        tracker = Tracker(provider)
        tracker.track_forward(
            start_frame=args.frame, show_result=args.show_result
        )
