#!/usr/bin/env python3

"""
Run this script after flashing the target drive with the OS image
This works for Raspbian images, and sets the cloud init files so that ssh, and wifi are configured on first boot

This script reads the templates - meta-data, user-data, and network-config, and replaces all RPI_* variables with values from the environment variables (also reads .env values)
If any RPI_* variables are still present after the replace pass (unresolved variables), it throws an error
Then it writes the replaced files to bootfs mounted directory (or any target path)
"""

import argparse
import os
import re
import shutil
from pathlib import Path
from dotenv import load_dotenv

FILES = ("meta-data", "user-data", "network-config")
VARIABLE = re.compile(r"\{\{RPI_[A-Za-z0-9_]+\}\}")


def replace_variables(text: str, values: dict[str, str], filename: str) -> str:
    missing = set()

    def replace(match: re.Match[str]) -> str:
        name = match.group(0)
        name = name.replace('{','').replace('}','')
        if name not in values:
            missing.add(name)
            return name
        return values[name]

    result = VARIABLE.sub(replace, text)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Unresolved variables in {filename}: {names}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Mounted bootfs directory")
    args = parser.parse_args()
    load_dotenv()

    if not args.target.is_dir():
        parser.error(f"Target directory does not exist: {args.target}")

    for name in FILES:
        source = Path(__file__).parent / name
        if not source.is_file():
            parser.error(f"Missing template: {source}")
        content = replace_variables(source.read_text(), dict(os.environ), str(source))
        destination = args.target / name
        destination.write_text(content)
        shutil.copystat(source, destination, follow_symlinks=True)


if __name__ == "__main__":
    main()
