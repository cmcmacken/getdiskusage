#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import logging
import platform
import re
import json
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("path", help="The Path we use to report disk usage on")
parser.add_argument("-u", "--unit",
                    default="b",
                    choices=["b", "m", "g"],
                    help="Unit used to report file size. b: byte, m: Mbyte, g: Gbyte")
parser.add_argument("-l", "--log-level",
                    choices=["INFO", "WARN", "ERROR", "DEBUG"],
                    default="WARN")

def parse_output(command_result, format="json"):
    file_list = []
    for line in command_result.stdout.split('\n'):
        if line != '':
            result = line.split('\t')

        file_list.append({result[1]: result[0]})

    output = ""
    if format == "json":
        output = json.dumps({"files": file_list}, indent=4)

    return output

def get_du_binary():
    du_name = "du"

    # choose the right du executable since OS X doesn't follow the standards
    if platform.system() == "Darwin":
        du_name = "gdu"
    elif platform.system() == "Windows":
        raise RuntimeError("The windows operating system is not supported at this time.")

    if not shutil.which(du_name):
        raise FileNotFoundError("The executable {} not found in $PATH".format(du_name))

    return du_name

def main():
    args = parser.parse_args()

    # convert to the value that logging expects
    log_level = getattr(logging, args.log_level.upper())

    # setup logging
    # this would be sent to a log file for some kind of log aggregation tool i.e. splunk
    logging.basicConfig(level=log_level)

    mount_point = Path(args.path).resolve()

    # ensure path exists
    if not mount_point.exists():
        message = "Path {} doesn't exist.".format(mount_point)
        logging.error(message)
        raise FileNotFoundError(message)

    # ensure the binary we need exists
    du_name = get_du_binary()

    output = subprocess.run(["/usr/bin/env",
                            du_name,
                            "-{}".format(args.unit),
                            "-a",
                            mount_point],
                            capture_output=True,
                            encoding='utf-8')

    json_output = parse_output(output)

    print(json_output)

if __name__ == '__main__':
    main()