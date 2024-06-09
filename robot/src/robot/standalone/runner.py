from robot.server.server_connector import clean
from robot.standalone.level_repository import get_level
from robot.logger import log_success


async def clean_level(robot_name: str, algo: str, level: str, speed: int):
    await clean({"robot_name": robot_name, "algo": algo, "level": get_level(level), "speed": speed})
    log_success("Press Enter to continue...")
    input()
