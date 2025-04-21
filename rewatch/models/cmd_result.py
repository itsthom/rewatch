from dataclasses import dataclass


@dataclass
class CmdResult:
    cmd: str
    elapsed_s: float | None = None
    stdout: str | None = None
    stderr: str | None = None
    returncode: int | None = None
    exception: Exception | None = None
