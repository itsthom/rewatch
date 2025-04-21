import asyncio
from typing import override

from rich.console import Group
from rich.live import Live
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from rewatch.cmder.abc import CmderAbc
from rewatch.cmder.run import run_cmd
from rewatch.models.cmd_result import CmdResult
from rewatch.models.options import Options


class CmderBars(CmderAbc):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self.overall_progress = self._overall_progress()
        self.overall_task = self.overall_progress.add_task(
            self._iter_task_name, total=self.iterations
        )
        self.task_progress = self._task_progress()
        self.live = self._live()

    @override
    def print_cmd_result(self, _result: CmdResult) -> None:
        pass

    @override
    async def iterate(self) -> None:
        with self.live:
            await super().iterate()

    @override
    async def _run_cmd(self) -> CmdResult:
        p_task = self.task_progress.add_task(self._cmd_task_name, total=None)
        result = await run_cmd(self.cmd, self.timeout)
        self.task_progress.update(p_task, advance=1, total=1, refresh=True)
        self.task_progress.remove_task(p_task)
        self.overall_progress.update(self.overall_task, advance=1, refresh=True)
        return result

    @override
    async def _sleep(self) -> None:
        if not self.delay:
            return

        steps = 100
        task = self.task_progress.add_task(self._sleep_task_name, total=steps)
        step = self.delay / steps
        for _ in range(steps):
            await asyncio.sleep(step)
            self.task_progress.update(task, advance=1, refresh=True)
        self.task_progress.remove_task(task)

    @property
    def _iter_task_name(self) -> str:
        return "[b]Iterations[/]"

    @property
    def _cmd_task_name(self) -> str:
        return f"Running cmd <{self.current_iteration}>..."

    @property
    def _sleep_task_name(self) -> str:
        return f"{self.delay}s delay..."

    def _overall_progress(self) -> Progress:
        return Progress(
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            BarColumn(bar_width=None),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            auto_refresh=False,
            expand=True,
        )

    def _task_progress(self) -> Progress:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            auto_refresh=False,
        )

    def _live(self) -> Live:
        return Live(
            Group(
                self.task_progress,
                self.overall_progress,
            ),
            refresh_per_second=30,
        )
