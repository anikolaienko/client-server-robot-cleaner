import asyncio

from aiohttp import web

from server.cli import parse_cli
from server.queue.queue_service import start_receiving
from server.robot.robot_connector import app, commands_executor


if __name__ == '__main__':
    cli_args = parse_cli()

    loop = asyncio.get_event_loop()
    loop.create_task(start_receiving(commands_executor.execute_command))

    web.run_app(app, loop=loop, port=cli_args.port)
