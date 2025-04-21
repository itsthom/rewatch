from typing import override

from rich.console import Console
from rich.live import Live

from rewatch.cmder.abc import CmderAbc
from rewatch.models.cmd_result import CmdResult
from rewatch.models.options import Options

SUCCESS = "."
FAILURE = "X"
ERROR = "E"
SHOULD_NOT_HAPPEN = "?"


class CmderDots(CmderAbc):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self._display = ""
        console = Console(emoji=False, highlight=False, markup=False, no_color=True)
        self._live = Live(
            self._display,
            auto_refresh=False,
            redirect_stderr=False,
            redirect_stdout=False,
            console=console,
        )

    @override
    def print_cmd_result(self, result: CmdResult) -> None:
        if result.exception:
            self._display += ERROR
        elif result.returncode == 0:
            self._display += SUCCESS
        elif result.returncode is not None:
            self._display += FAILURE
        else:
            self._display += SHOULD_NOT_HAPPEN

        self._live.update(self._display, refresh=True)

    @override
    async def iterate(self) -> None:
        with self._live:
            await super().iterate()
