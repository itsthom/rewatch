import json
from typing import override

from rich.console import Console

from rewatch.cmder.abc import CmderAbc
from rewatch.models.cmd_result import CmdResult
from rewatch.models.options import Options


class CmderJson(CmderAbc):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self._console = Console(
            emoji=False, highlight=False, markup=False, no_color=True
        )

    @override
    def print_cmd_result(self, result: CmdResult) -> None:
        result_dict: dict[str, str | int | None] = {
            "iteration": self.current_iteration,
            "cmd": result.cmd,
            "returncode": result.returncode,
        }
        if result.stderr and self.print_stderr:
            result_dict["stderr"] = result.stderr
        if result.stdout:
            result_dict["stdout"] = result.stdout
        if result.exception:
            result_dict["exception"] = str(result.exception)

        self._console.print_json(json.dumps(result_dict), indent=None)
