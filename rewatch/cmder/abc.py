import asyncio
from abc import ABC, abstractmethod

from rewatch.cmder.run import run_cmd
from rewatch.models.cmd_result import CmdResult
from rewatch.models.options import Options


class CmderAbc(ABC):
    def __init__(self, options: Options) -> None:
        # Command Options
        self.cmd = " ".join(options.command)
        self.delay = options.delay
        self.iterations = options.iterations
        self.timeout = options.timeout
        # Output Options
        self.output_mode = options.output_mode
        self.print_stderr = options.print_stderr
        self.print_stdout = options.print_stdout
        # Results
        self.current_iteration = 0
        self.return_codes: dict[int | None, int] = {}
        self.exceptions: dict[type[Exception], int] = {}

    @abstractmethod
    def print_cmd_result(self, result: CmdResult) -> None:
        raise NotImplementedError("Subclasses must implement print_cmd_result method")

    async def iterate(self) -> None:
        for i in range(self.iterations):
            self.current_iteration = i + 1
            result = await self._run_cmd()
            self.print_cmd_result(result)
            self.return_codes[result.returncode] = (
                self.return_codes.get(result.returncode, 0) + 1
            )
            if result.exception:
                self.exceptions[type(result.exception)] = (
                    self.exceptions.get(type(result.exception), 0) + 1
                )

            if i < self.iterations - 1:
                await self._sleep()

    async def _run_cmd(self) -> CmdResult:
        return await run_cmd(self.cmd, self.timeout)

    async def _sleep(self) -> None:
        if not self.delay:
            return
        await asyncio.sleep(self.delay)
