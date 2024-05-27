from dataclasses import dataclass
from typing import Optional

from server.models.execution_status import ExecutionStatus


@dataclass
class ExecutionResult:
    status: ExecutionStatus
    error: Optional[str] = None
