# Stripe-Client-Config-Checker
Checks client's Stripe configs to ensure all settings match required configs for Stripe migration

## How to Run
Usage:
```
python3 checkConfig.py [-h] [-a A_ID] [-t CLIENTTYPE] [-f PARSEFILE] [-c CLIENTTYPECHART]
```
Options:
```
  -h, --help                        show this help message and exit
  -a, --acct A_ID                   <str> account_id of the client
  -t, --client-type CLIENTTYPE      <int> what type of client they are (1, 2, 3, 4)
  -f, --file PARSEFILE              <path> OPTIONAL: path to csv file to parse data from
  -c, --chart CLIENTTYPECHART       <path> OPTIONAL: path to csv file containing the chart of rules for what configs need to be set per client type
```
The script expects the following default file tree unless otherwise specified by passing the `-f` or `-c` options:
```
project/
    ├── clientTypeChart.csv
    ├── export.csv
    └── checkConfig.py
```

## TODO
function docstrings
