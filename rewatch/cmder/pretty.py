from datetime import timedelta
from time import perf_counter
from typing import override

from rich.pretty import Pretty
from rich.table import Table

from rewatch.cmder.bars import CmderBars
from rewatch.models.cmd_result import CmdResult


class CmderPretty(CmderBars):
    @override
    def print_cmd_result(self, result: CmdResult) -> None:
        table = self._result_to_table(result)
        table.title = f"Iteration {self.current_iteration} of {self.iterations}"
        renderables = ["\n", table]
        if self.current_iteration == self.iterations:
            renderables.append("\n")
        self.live.console.print(*renderables)

    @override
    async def iterate(self) -> None:
        self.start_time = perf_counter()
        await super().iterate()
        self.end_time = perf_counter()
        self._print_summary()

    def _result_to_table(self, result: CmdResult) -> Table:
        border = (
            None
            if result.returncode is None
            else "red" if result.returncode else "green"
        )

        table = Table(
            border_style=border,
            show_header=False,
            show_lines=True,
            title_style="bold italic magenta",
        )
        table.add_row("Command", Pretty(result.cmd))
        table.add_row("Return Code", Pretty(result.returncode))
        if result.stdout and self.print_stdout:
            table.add_row("STDOUT", result.stdout)
        if result.stderr and self.print_stderr:
            table.add_row("STDERR", result.stderr)
        if result.exception:
            table.add_row("Exception", Pretty(result.exception))

        return table

    def _print_summary(self) -> None:
        elapsed = self.end_time - self.start_time
        elapsed_td = timedelta(seconds=elapsed)

        table = Table(
            show_header=False,
            show_lines=True,
            title="Summary",
            title_style="bold italic magenta",
        )
        table.add_row("[b yellow]Iterations[/]", Pretty(self.iterations))
        table.add_row("[b yellow]Duration[/]", f"[b cyan]{elapsed_td}[/]")
        for exc, count in self.exceptions.items():
            table.add_row(f"[b red]Exception: {exc}[/]", Pretty(count))
        for rc, count in self.return_codes.items():
            rc_style = "b red" if rc else "b green"
            table.add_row(f"[{rc_style}]Return Code: {rc}[/]", Pretty(count))

        self.live.console.print("\n", table, "\n")
