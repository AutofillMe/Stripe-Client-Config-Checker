import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument(
    "-a",
    "--acct",
    dest="a_id",
    help="account_id of the client",
)

parser.add_argument(
    "-t",
    "--client-type",
    dest="clientType",
    type=int,
    help="what type of client they are (1, 2, 3, 4)",
)

parser.add_argument(
    "-f",
    "--file",
    dest="parseFile",
    type=Path,
    help="path to csv file to parse data from",
)

args = parser.parse_args()


def parseClientTypeChart(path: Path, clientType: int) -> dict:
    req: dict = {}

    if clientType == 1:
        print()
    if clientType == 2:
        print()
    if clientType == 3 or clientType == 4:
        print()
    return req


def configCheck():
    return None


def main(args: argparse.Namespace) -> int | None:
    parseFile: Path = args.parseFile
    clientType: int = args.clientType
    account_id: str = args.a_id
    configCheck()
    return 0


if __name__ == "__main__":
    main(args)
