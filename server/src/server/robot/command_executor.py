import inspect

import socketio

from server.models import ExecutionStatus, ExecutionResult
from server.level_provider import get_level
from server.exceptions import ExecutionError


class CommandExecutor:
    def __init__(
            self,
            sio: socketio.AsyncServer,
            robot_name_to_sid: dict[str, str]
            ):
        self._sio = sio
        self._robot_name_to_sid = robot_name_to_sid
        self._commands_registry = {
            "clean": self.run_clean_level,
            "pause": self.run_pause_work,
            "resume": self.run_resume_work,
            "reset": self.run_reset,
            "speed": self.run_change_speed,
            "version": self.version_broadcast,
        }

    def _get_sid(self, robot_name: str) -> str:
        sid = self._robot_name_to_sid.get(robot_name)
        if sid is None:
            raise ExecutionError(f"No robot with name `{robot_name}` is connected.")
        return sid

    async def run_clean_level(self, robot: str, level: str, speed: int = 1):
        sid = self._get_sid(robot)
        level_structure = get_level(level)
        if level_structure is None:
            raise ExecutionError(f"No level `{level}` found.")
        
        data = {
            "level": level_structure,
            "speed": speed
        }

        await self._sio.emit("clean", data=data, to=sid)

    async def run_pause_work(self, robot: str):
        await self._sio.emit("pause", to=self._get_sid(robot))

    async def run_resume_work(self, robot: str):
        await self._sio.emit("resume", to=self._get_sid(robot))

    async def run_reset(self, robot: str):
        await self._sio.emit("reset", to=self._get_sid(robot))

    async def run_change_speed(self, robot: str, value: int):
        await self._sio.emit("speed", data={"value": value}, to=self._get_sid(robot))
    
    async def version_broadcast(self):
        await self._sio.emit("version")

    async def execute_command(self, command_name: str, data: dict[str, str]) -> ExecutionStatus:
        if command_name not in self._commands_registry:
            return ExecutionResult(ExecutionStatus.ERROR, f"Command `{command_name}` is not registered.")
        
        command = self._commands_registry[command_name]
        
        try:
            await command(**data)
            return ExecutionResult(ExecutionStatus.SUCCESS)
        except TypeError as ex:
            expected_args = inspect.getfullargspec(command).annotations
            return ExecutionResult(
                ExecutionStatus.ERROR,
                f"Command `{command_name}` expects arguments: {expected_args}\nReceived: {data}"
            )
        except ExecutionError as ex:
            return ExecutionResult(ExecutionStatus.ERROR, str(ex))
        except Exception as ex:
            return ExecutionResult(ExecutionStatus.ERROR, f"Unexpected Error: {ex}")
