import asyncio

from robot.cli import parse_cli
from robot.server.server_connector import connect_to_server
from robot.standalone.runner import clean_level
from robot.logger import keep_alive


if __name__ == '__main__':
    cli_args = parse_cli()
    
    with keep_alive():
        if cli_args.standalone:
            asyncio.run(clean_level(cli_args.name, cli_args.level, cli_args.speed))
        else:
            asyncio.run(connect_to_server(cli_args.port, cli_args.name, cli_args.speed))
