import asyncio

from robot.cli import parse_cli
from robot.server.server_connector import connect_to_server, execute_algo
from robot.logger import keep_alive


if __name__ == '__main__':
    cli_args = parse_cli()
    
    with keep_alive():
        # asyncio.run(connect_to_server(cli_args.port, cli_args.name))
        asyncio.run(execute_algo(cli_args.name))
