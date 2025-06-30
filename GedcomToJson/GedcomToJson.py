import logging
import os
from argparse import ArgumentParser
from enum import Enum


class ReturnCode(Enum):
    ERR_OK = 0
    ERR_READ_INPUT_FILE = -1
    ERR_WRITE_OUTPUT_FILE = -2
    ERR_UNSUPPORTED_VERSION = -3
    ERR_VERS_NOT_IN_FILE = -10


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
            return ["-1", ""]
        return splitted_line

    def _check_version(self) -> int:
        if self._version not in self._SUPPORTED_VERSIONS:
            logging.error(f'Unsupported version {self._version}')
            return ReturnCode.ERR_UNSUPPORTED_VERSION.value
        return ReturnCode.ERR_OK.value

    def _verify_version_in_file(self) -> int:
        for line in self._input_file_array:
            line_list = self._parse_one_line(line)
            if line_list[0] == 2 and "VERS" in line_list[1]:
                self._version = line_list[1].strip(" ")[1]
                return self._check_version()
        logging.error("VERS not in file")
        return ReturnCode.ERR_VERS_NOT_IN_FILE.value

    def check_file(self):
        return_code = self._verify_version_in_file()
        if not return_code:
            return return_code
        return ReturnCode.ERR_OK.value

    def parse(self):
        for raw_line in self._input_file_array:
            # TODO here
            pass
        return ReturnCode.ERR_OK.value


def main(file_path: str) -> int:
    gedcom_parser = GedcomParser(file_path)
    return_code = gedcom_parser.check_file()
    if not return_code:
        return return_code

    return_code = gedcom_parser.parse()
    if not return_code:
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

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)

    logging.info("JSON to GEDCOM")
    status = main(args.file)
    os._exit(status)
