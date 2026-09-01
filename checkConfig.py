import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument(
    "-a",
    "--acct",
    dest="a_id",
    help="<str> account_id of the client",
)

parser.add_argument(
    "-t",
    "--client-type",
    dest="clientType",
    type=int,
    help="<int> what type of client they are (1, 2, 3, 4)",
)

parser.add_argument(
    "-f",
    "--file",
    dest="parseFile",
    type=Path,
    help="<path> path to csv file to parse data from",
)

parser.add_argument(
    "-c",
    "--chart",
    dest="clientTypeChart",
    type=Path,
    help="<path> path to csv file containing the chart of rules for what configs need to be set per client type",
)

args = parser.parse_args()


def createDictKeys(req: dict, keyLine: list[str]) -> dict[str, list]:
    for key in keyLine:
        req[key] = []
    return req


def appendDictItems(req: dict, line: str, keys: list[str]) -> dict[str, list[str]]:
    itemsToAppend: list[str] = line.strip().split(",", maxsplit=3)
    count: int = 0
    for key in keys:
        req[key].append(itemsToAppend[count])
        count += 1
    return req


def parseClientTypeChart(
    clientTypeChart: Path, clientType: int
) -> dict[str, list[str]]:
    req: dict = {}

    # TODO this shit ugly, need to clean
    with open(clientTypeChart, "r") as f:
        for line in f:
            if line[2] == str(clientType):
                keys = f.readline().strip().split(",")
                req = createDictKeys(req, keys)
                for line in f:
                    if line.strip() == "$END":
                        return req
                    req = appendDictItems(req, line, keys)

    return req


def passFail(row: pd.DataFrame, req: dict[str, list[str]]) -> None:
    return


def configCheck(
    account_id: str,
    clientType: int,
    parseFile: Path,
    clientTypeChart: Path,
) -> None:
    if not parseFile.is_file():
        print(
            "Failed to open export.csv, please check that the file exists at the given path or the default path of ./export.csv"
        )
        print(f"Path to export.csv: {parseFile}")
        raise SystemExit(1)

    if not clientTypeChart.is_file():
        print(
            "Failed to open clientTypeChart.csv, please check that the file exists at the given path or the default path of ./clientTypeChart.csv"
        )
        print(f"Path to rules.csv: {clientTypeChart}")
        raise SystemExit(1)

    if account_id == None:
        print("Please provide an account ID to check.")
        raise SystemExit(1)

    if clientType == None:
        print("Please provide a client type to check.")
        raise SystemExit(1)

    df: pd.DataFrame = pd.read_csv(parseFile, dtype="string")
    # When reading in the export file, column 0 should always
    # be account_id after being passed through the standardizer
    row: pd.DataFrame = df[df.iloc[:, 0] == account_id].iloc[0]
    req: dict[str, list[str]] = parseClientTypeChart(clientTypeChart, clientType)
    passFail(row, req)
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
