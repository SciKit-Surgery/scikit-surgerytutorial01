# coding=utf-8

"""Command line processing"""


import argparse
from snappytutorial01 import __version__
from snappytutorial01.ui.snappytutorial01_demo import run_demo


def main(args=None):
    """Entry point for SNAPPYTutorial01 application"""

    parser = argparse.ArgumentParser(description='SNAPPYTutorial01')

    parser.add_argument("-t", "--text",
                        required=False,
                        default="This is SNAPPYTutorial01",
                        type=str,
                        help="Text to display")

    parser.add_argument("--console", required=False,
                        action='store_true',
                        help="If set, SNAPPYTutorial01 "
                             "will not bring up a graphical user interface")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "-v", "--version",
        action='version',
        version='SNAPPYTutorial01 version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.console, args.text)
