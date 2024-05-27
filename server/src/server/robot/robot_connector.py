from typing import Any

import socketio
from aiohttp import web

from server.robot.command_executor import CommandExecutor

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

robot_name_to_sid: dict[str, str] = dict()

commands_executor = CommandExecutor(sio, robot_name_to_sid)


@sio.event
async def connect(sid, environ: dict[str, Any], auth: str):
    name = auth

    await sio.save_session(sid, {'robot_name': name})
    robot_name_to_sid[name] = sid
    
    print(f"connected robot `{name}` with sid `{sid}`")


@sio.event
async def disconnect(sid):
    async with sio.session(sid) as session:
        name = session["robot_name"]
        robot_name_to_sid.pop(name)

        print(f"disconnected robot {name} with sid {sid}")


@sio.event
async def error(sid, error_msg: str):
    async with sio.session(sid) as session:
        robot_name = session["robot_name"]
        print(f"Robot `{robot_name}` reported error: {error_msg}")
        # TODO: push to Kafka streams


@sio.event
async def robot_version(sid, version: str):
    async with sio.session(sid) as session:
        robot_name = session["robot_name"]
        print(f"Robot `{robot_name}` firmware version: {version}")
