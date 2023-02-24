import argparse
import logging
import sys
import os

from typing import Optional

class InputParser(argparse.ArgumentParser):

    def error(self, message: str):
        logging.error(f"Error: {message}")
        self.print_help()
        sys.exit(2)

def check_if_path_exists(
    input_parser: InputParser,
    input_path: str
) -> Optional[str]:
    """Check if passed path exists

    :param input_parser: ArgumentParser modified instance 
    :type input_parser: InputParser
    :param input_path: Inserted path
    :type input_path: str
    :return: Input path if valid
    :rtype: str
    """

    if os.path.exists(input_path):
        return input_path
    input_parser.error(f"Input path {input_path} does not exist!")

def create_if_does_not_exist(
    input_path: str
) -> Optional[str]:
    """Create input path if it doesn't exist

    :param input_path: Inserted path
    :type input_path: str
    :return: Input path
    :rtype: str
    """

    os.makedirs(input_path, exist_ok=True)
    return input_path


def parse_arguments() -> argparse.Namespace:
    parser = InputParser()
    parser.add_argument(
        "data_path",
        help="Path to file with text input for GPT",
        metavar="Input",
        type=lambda path: check_if_path_exists(parser, path)
    )

    parser.add_argument(
        "-c", "--cookies_path",
        help="Optional. A path to cookies file stored from Chromium",
        dest="cookies",
        default="snap/chromium/common/chromium/Default/Cookies", 
        # or .config/google-chrome/Default/Cookies 
    )

    parser.add_argument(
        "-o", "--output",
        help="Optional. Output folder, default output",
        dest="output",
        default="gpt-output",
        type=lambda path: create_if_does_not_exist(path)
    )

    parser.add_argument(
        '-t',
        '--token',
        help="Optional. Auth token for GPT API. If provided, cookies_path is ignored.",
        dest="token",
    )

    parser.add_argument(
        '--token-path',
        help="Optional. Auth token for GPT API. If provided, cookies_path and --token argument is ignored.",
        dest="token_path",
    )

    parser.add_argument(
        '-g',
        '--gen-id-column',
        help="Optional. Generate ID column if is not present in the input data. Default: False",
        dest="generate",
        action="store_true",
        default=False
    )

    parser.add_argument(
        '-n',
        '--column-names',
        help="""Optional. Column names to use. Only two columns are neccessary, 
            prompt - question for GPT and id - id of text.
        """,
        dest="columns",
        nargs=2,
        default=["prompt", "id"]
    )

    parser.add_argument(
        "-v", "--verbose",
        help="Optional. Change log level",
        choices=("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"),
        default="INFO",
        dest="verbose"
    )

    parser.add_argument(
        "-s", "--start",
        help="Optional. Start processing from text with provided index.",
        default=0,
        type=int,
        dest="start",
    )

    parser.add_argument(
        "-sc", "--separate-conversations",
        help="Optional. Send one text per one conversation.",
        default=False,
        action="store_true",
        dest="sep",
    )

    return parser.parse_args()