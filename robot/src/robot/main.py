import asyncio

from robot.cli import parse_cli
from robot.server.server_connector import connect_to_server
from robot.logger import keep_alive


if __name__ == '__main__':
    cli_args = parse_cli()
    
    with keep_alive():
        asyncio.run(connect_to_server(cli_args.server_id, cli_args.name))
