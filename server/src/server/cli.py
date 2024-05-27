from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class CLIArgs:
    port: int


def parse_cli() -> CLIArgs:
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True)
    args = parser.parse_args()

    return CLIArgs(**vars(args))
