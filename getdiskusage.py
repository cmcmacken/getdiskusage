#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import platform
import re
import json
import shutil


def parse_output(command_result, format="json"):
    """
    Parse the output of our du command into a basic datastructure and convert it to the output format we want

    """

    file_list = []
    for line in command_result.stdout.split('\n'):
        if line == '':
            continue
        elif "\t" not in line:
            raise ValueError(
                "Output from disk usage executable is not what we expected.")

        result = re.search(r"(\d+)\s+(.+)", line)

        if not result:
            raise ValueError(
                "Output from disk usage executable is not what we expected.")

        file_size = result.group(1)
        file_name = result.group(2)
        file_list.append({file_name: file_size})

    output = ""
    if format == "json":
        output = json.dumps({"files": file_list}, indent=4)

    return output


def get_du_binary():
    """
    Support some different platforms, specifically Mac OSX since it doesn't have GNU du installed
    """
    du_name = "du"

    # choose the right du executable since OS X doesn't follow the standards
    if platform.system() == "Darwin":
        du_name = "gdu"
    elif platform.system() == "Windows":
        raise RuntimeError(
            "The windows operating system is not supported at this time.")

    if not shutil.which(du_name):
        raise FileNotFoundError(
            "The executable was not found in the $PATH", du_name)

    return du_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The Path we use to report disk usage on")
    parser.add_argument("-u", "--unit",
                        default="b",
                        choices=["b", "m", "g"],
                        help="Unit used to report file size. b: byte, m: Mbyte, g: Gbyte")

    args = parser.parse_args()

    mount_point = Path(args.path).resolve()

    # ensure path exists
    if not mount_point.exists():
        raise FileNotFoundError("Path doesn't exist.", mount_point)

    # ensure the binary we need exists
    du_name = get_du_binary()

    output = subprocess.run(["/usr/bin/env",
                            du_name,
                            "-{}".format(args.unit),
                            "-a",
                            mount_point],
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    output = parse_output(output)
    print(output)


if __name__ == '__main__':
    main()
