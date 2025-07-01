import logging
import sys
import os
from argparse import ArgumentParser
from enum import Enum


class MyFormatter(logging.Formatter):
    error_fmt = "[x] %(message)s"
    warning_fmt = "[!] %(message)s"
    info_fmt = "[-] %(message)s"
    debug_fmt = "[*] %(message)s"

    def __init__(self):
        super().__init__()

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = MyFormatter.debug_fmt
        elif record.levelno == logging.INFO:
            self._style._fmt = MyFormatter.info_fmt
        elif record.levelno == logging.WARNING:
            self._style._fmt = MyFormatter.warning_fmt
        elif record.levelno == logging.ERROR:
            self._style._fmt = MyFormatter.error_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


class ReturnCode(Enum):
    ERR_OK = 0
    ERR_READ_INPUT_FILE = 1
    ERR_WRITE_OUTPUT_FILE = 2
    ERR_UNSUPPORTED_VERSION = 3
    ERR_VERS_NOT_IN_FILE = 10


class GedcomParser():
    def __init__(self, input_file_path: str) -> None:
        self._SUPPORTED_VERSIONS = ['5.5.5']
        with open(input_file_path, 'r') as input_file_stream:
            self._input_file_array = input_file_stream.readlines()
        if self._input_file_array == None:
            logging.error(f'Cannot read {input_file_path}')
            os._exit(ReturnCode.ERR_READ_INPUT_FILE.value)

    def _parse_one_line(self, line: str):
        rstripped_line = line.rstrip("\n").rstrip(
            '\r').rstrip(" ")
        splitted_line = rstripped_line.split(' ', 1)
        if len(splitted_line) != 2 or rstripped_line != f"{splitted_line[0]} {splitted_line[1]}":
            logging.warning(f"Could not parse line {line}")
            return [-1, ""]
        cast_splitted_line = [int(splitted_line[0]), splitted_line[1]]
        return cast_splitted_line

    def _check_version(self) -> int:
        if self._version not in self._SUPPORTED_VERSIONS:
            logging.error(f'Unsupported version {self._version}')
            return ReturnCode.ERR_UNSUPPORTED_VERSION.value
        logging.debug(f'GEDCOM Version {self._version}')
        return ReturnCode.ERR_OK.value

    def _verify_version_in_file(self) -> int:
        for line in self._input_file_array:
            line_list = self._parse_one_line(line)
            if line_list[0] == 2 and "VERS" in line_list[1]:
                self._version = line_list[1].split(" ")[1]
                return self._check_version()
        logging.error("VERS not in file")
        return ReturnCode.ERR_VERS_NOT_IN_FILE.value

    def check_file(self):
        return_code = self._verify_version_in_file()
        if return_code:
            return return_code
        return ReturnCode.ERR_OK.value

    def parse(self):
        for raw_line in self._input_file_array:
            line_list = self._parse_one_line(raw_line)

            pass
        return ReturnCode.ERR_OK.value


def main(file_path: str) -> int:
    gedcom_parser = GedcomParser(file_path)
    return_code = gedcom_parser.check_file()
    if return_code:
        return return_code

    logging.info('GEDCOM file OK')

    return_code = gedcom_parser.parse()
    if return_code:
        return return_code
    return ReturnCode.ERR_OK.value


if __name__ == '__main__':
    parser = ArgumentParser()
    parser._optionals.title = "Options"
    parser.add_argument("-f", "--file", action='store',
                        help="GEDCOM file", required=True)
    parser.add_argument("-d", "--debug", action='store_true',
                        help="debug mode", required=False)
    args = parser.parse_args()

    # Custom logging formatter
    my_formatter = MyFormatter()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(my_formatter)
    logging.root.addHandler(handler)

    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    logging.info("JSON to GEDCOM")
    status = main(args.file)
    os._exit(status)
