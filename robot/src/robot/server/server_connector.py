import asyncio
import traceback

import socketio
import socketio.exceptions

from robot.version import get_version
from robot.logger import log, log_success, log_error, log_warning, display_level
from robot.algos.clean_algos import ALGOS
from robot.types import LevelType
from robot.models import RobotState, Stats, Direction
from robot.utils.level_parser import parse_level

sio = socketio.AsyncClient()
state = RobotState()


async def connect_to_server(server_port: str, robot_name: str, speed: int):
    state.name = robot_name
    state.speed = speed
    server_url = f"http://0.0.0.0:{server_port}/"
    
    await sio.connect(server_url, auth=robot_name)
    await sio.wait()

@sio.event
async def connect():
    log_success('Connection established')

@sio.event
async def disconnect():
    log_success('Disconnected from server')


async def cleaning_refresh(level: LevelType, stats: Stats, direction: Direction) -> bool:
    display_level(level, stats, direction)

    if state.reset:
        return False
    
    if not state.paused:
        await asyncio.sleep(state.delay)
    else:
        while state.paused:
            await asyncio.sleep(state.delay)
    
    return True

@sio.event
async def clean(data: dict[str, str]):
    state.reset = False

    if state.name is None:
        state.name = data.get("robot_name")
    
    if state.cleaning:
        msg = "Received another `clean` command while already cleaning."
        log_error(msg)
        await sio.emit("error", msg)
        return

    level_str = data.get("level")
    if level_str is None:
        error_msg = "Failed `clean` command. Expected `level` argument not found."
        log_error(error_msg)
        await sio.emit("error", error_msg)
        return
    
    if "speed" in data:
        state.speed = int(data["speed"])

    algo_name = data.get("algo")
    if algo_name is None:
        algo_name, algo_runner = next(iter(ALGOS.items()))
        log_warning(f"No algo specified. Random choice: `{algo_name}`")
    elif algo_name not in ALGOS:
        log_error(f"Algo with name `{algo_name}` not found. Please use one the following: {ALGOS.keys()}")
        return
    else:
        algo_runner = ALGOS[algo_name]
    
    log_success(f"Running cleaning algo `{algo_name}` with speed {state.speed} ...")
    try:
        state.cleaning = True

        level = parse_level(level_str)
        is_cleaned = await algo_runner(state.name, level, cleaning_refresh)

        if is_cleaned:
            log_success("Done", "Level is cleaned successfully.")
        else:
            if state.reset:
                state.reset = False
                log_warning("Stopped cleaning.")
            else:
                log_warning("Partially cleaned. Some parts of level are not accessible.")
    except Exception as ex:
        log_error(f"Failed to clean the level. Error: {ex}\nTrace:{traceback.extract_tb(ex.__traceback__)}")
    finally:
        state.cleaning = False

@sio.event
async def pause():
    if state.cleaning:
        state.paused = True
        log_success("Paused")
        return
    log_warning("Received `pause` but was not cleaning.")

@sio.event
async def resume():
    if state.paused:
        state.paused = False
        log_success("Resumed cleaning...")
        return
    log_warning("Received `resume` but was not paused.")

@sio.event
async def reset():
    if state.cleaning:
        state.reset = True
        log_success("Stopped cleaning completely")
        return
    log_warning("Received `reset` but was not cleaning.")

@sio.event
async def speed(data: dict[str, str]):
    error_msg = None
    speed_value = data.get("value")

    if speed_value is None:
        error_msg = "Failed `clean` command. Expected `level` argument not found."
    else:
        try:
            state.speed = int(speed_value)
            log(f"Speed: {speed_value}")
        except ValueError as ex:
            error_msg = str(ex)
        
    if error_msg:
        log_error(error_msg)
        await sio.emit("error", error_msg)


@sio.event
async def version():
    await sio.emit("robot_version", get_version())
    log_success("Sent firmware version")
