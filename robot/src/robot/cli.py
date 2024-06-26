from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Optional


@dataclass
class CLIArgs:
    name: str
    speed: int
    standalone: bool
    port: Optional[str]
    level: Optional[str]
    algo: Optional[str]


def parse_cli() -> CLIArgs:
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-s", "--speed", default=1)
    
    parser.add_argument("-S", "--standalone", action='store_true', default=False)
    parser.add_argument("-p", "--port", default=None)
    parser.add_argument("-l", "--level", default=None)
    parser.add_argument("-a", "--algo", default=None)

    args = parser.parse_args()

    cli_args = CLIArgs(**vars(args))
    if cli_args.standalone:
        assert cli_args.port == None, "`port` should not be specified in standalone mode"
        assert cli_args.level != None, "`level` should be specified in standalone mode"
        assert cli_args.algo != None, "`algo` should be specified in standalone mode"
    else:
        assert cli_args.level == None, "`level` should not be specified in client mode"
        assert cli_args.algo == None, "`algo` should not be specified in client mode"
        assert cli_args.port != None, "`port` should be specified in client mode"
    
    return cli_args
