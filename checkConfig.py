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


def createDictKeys(req: dict, keys: list[str]) -> dict[str, list]:
    """
    Task:
    Custom logic for creating the empty requirement dict based on the items:
    Name of Setting (Human readable), name of setting (variable name), expected result, fix
    ---
    IN: empty dictionary
    IN: list containing the item keys
    OUT: dict with keys
    """
    for key in keys:
        req[key] = []
    return req


def appendDictItems(req: dict, line: str, keys: list[str]) -> dict[str, list[str]]:
    """
    Tasks:
    Since the line containing the recommended fix to the client already contains commas,
    the line needs to be cleaned and appended in order to requirement dict
    ---
    Note:
    The current format is:
    Name of Setting (Human readable), name of setting (variable name), expected result, fix
    ---
    IN: the requirement dict
    IN: the unformatted line (str)
    IN: the list of keys as in the note above, so that each item is assigned to the correct dict item. (list[str])
    OUT: the requirement dict with the new entry added
    """
    itemsToAppend: list[str] = line.strip().split(",", maxsplit=3)
    for index, key in enumerate(keys):
        req[key].append(itemsToAppend[index])
    return req


def parseClientTypeChart(
    clientTypeChart: Path, clientType: int
) -> dict[str, list[str]]:
    """
    Task:
    Parses the client type chart to create a dict containing all the required configs
    ---
    Note:
    the client type chart requires particular formatting, WIP autoformatter
    ---
    IN: path to client type chart csv file (Path)
    IN: client type (int)
    OUT: all requirements for given client type (dict)
    """
    req: dict = {}

    # TODO this shit ugly, need to clean
    with open(clientTypeChart, "r") as f:
        for line in f:
            if line[2] == str(clientType):
                print(f"Client Type: {line[6:]}")
                keys = f.readline().strip().split(",")
                req = createDictKeys(req, keys)
                for line in f:
                    if line.strip() == "$END":
                        return req
                    req = appendDictItems(req, line, keys)

    return req


def checkPassFail(row: pd.DataFrame, req: dict[str, list[str]]) -> None:
    """
    Task:
    Given an account id and the requirements for a given client type, print
    pass/fail, and upon fail, print why and corrections to be done
    ---
    Note:
    The statements use emojis, so some terminals may not have emoji support
    ---
    IN: a single row DataFrame containing the selected settings for a given acct id
    IN: the list of required settings to validate against (dict)
    OUT: None
    """
    fixes: list[list[str]] = []
    incorrectSettings: list[list[str]] = []

    # compare config vs expected values and add them to lists for printing
    for index, col in enumerate(req["Column Name"]):
        if row[col].lower() != req["Expected Response"][index]:
            fixes.append([req["Stripe Setting"][index], req["Guide for client"][index]])
            incorrectSettings.append(
                [
                    req["Stripe Setting"][index],
                    req["Expected Response"][index],
                    str(row[col]),
                ]
            )

    # if fixes are empty
    if not fixes:
        print("Stripe configuration is set correctly! ✅")
    # if fixes not empty
    else:
        print(
            f"Stripe configuration is not correct! ❌\nThere are {len(fixes)} fixes that need to addressed.\n"
        )
        # print expected vs actual configs
        for i in incorrectSettings:
            print(
                f"Incorrect Setting: {i[0]}\n\t✅ Expected Response: {i[1]}\n\t❌ Actual Response: {i[2]}"
            )

        # print fixes to copy paste to client
        print("Fixes to apply:")
        for i in fixes:
            print(
                f"\t{i[0]}:\n\t\t{i[1].replace('\\n', '\n\t\t').replace('""', '"')}\n\n"
            )
    return


def configCheck(
    account_id: str,
    clientType: int,
    parseFile: Path,
    clientTypeChart: Path,
) -> None:
    """
    Task:
    Takes an account id, the client type, Stripe export file and client type chart,
    parses the given account id to find any missing or incorrect settings and prints them to stdout
    ---
    Notes:
    WIP: account id string validation, more verbose client type declaration
    ---
    IN: Stripe account id (should look like acct_xxxxxxx) (str)
    IN: client type as per the chart (int)
    IN: path to most recent Stripe export file to parse (Path)
    IN: path to client type chart containing the required settings (Path)
    OUT: None
    """
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
    checkPassFail(row, req)
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
