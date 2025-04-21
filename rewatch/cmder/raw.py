from typing import override

from rich.console import Console
from rich.rule import Rule

from rewatch.cmder.abc import CmderAbc
from rewatch.models.cmd_result import CmdResult
from rewatch.models.options import Options


class CmderRaw(CmderAbc):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self._console = Console(emoji=False, highlight=False, markup=False)
        self._err_console = Console(
            emoji=False, highlight=False, markup=False, stderr=True
        )

    @override
    def print_cmd_result(self, result: CmdResult) -> None:
        rule_title = f"{self.current_iteration} of {self.iterations}"
        self._console.print("", Rule(rule_title), "")
        if result.exception:
            self._err_console.print(f"Exception: {result.exception}")
        if result.stderr and self.print_stderr:
            self._err_console.print(result.stderr)
        if result.stdout and self.print_stdout:
            self._console.print(result.stdout)
