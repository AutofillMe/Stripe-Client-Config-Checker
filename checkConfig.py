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

parser.add_argument(
    "-c",
    "--chart",
    dest="clientTypeChart",
    type=Path,
    help="path to csv file containing the chart of rules for what configs need to be set per client type",
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


def configCheck(
    account_id: str,
    clientType: int,
    parseFile: Path,
    rulesFile: Path,
) -> None:
    if not parseFile.is_file():
        print("Failed to open export.csv, please check that the file exists at the given path or the default path of ./export.csv")
        print(f"Path to export.csv: {parseFile}")
    
    if not rulesFile.is_file():
        print("Failed to open rules.csv, please check that the file exists at the given path or the default path of ./rules.csv")
        print(f"Path to rules.csv: {rulesFile}")

    df: pd.DataFrame = pd.read_csv(parseFile, dtype="string")
    row: pd.DataFrame = df[df.iloc[:, 0] == account_id].iloc[0]
    return None


def main(args: argparse.Namespace) -> int | None:
    account_id: str = args.a_id
    clientType: int = args.clientType
    parseFile: Path = args.parseFile or Path("./export.csv")
    clientTypeChart: Path = args.clientTypeChart or Path("./clientTypeChart.csv")
    configCheck(account_id, clientType, parseFile, clientTypeChart)
    return 0


if __name__ == "__main__":
    main(args)
