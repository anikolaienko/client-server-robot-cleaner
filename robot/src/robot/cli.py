from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class CLIArgs:
    name: str
    port: str


def parse_cli() -> CLIArgs:
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-p", "--port", required=True)
    args = parser.parse_args()

    return CLIArgs(**vars(args))
