import asyncio

from rich.console import Console
from typer import Typer

from rewatch.cmder.factory import Cmder
from rewatch.models.options import Options
from rewatch.models.output_mode import OutputMode
from rewatch.options import (
    Command,
    Delay,
    Iterations,
    Output,
    PrintStdErr,
    PrintStdOut,
    Timeout,
)

app = Typer(rich_markup_mode="rich")


@app.command(context_settings={"ignore_unknown_options": True})
def main(
    iterations: Iterations,
    command: Command,
    delay: Delay = 0.0,
    timeout: Timeout = 30.0,
    output: Output = OutputMode.PRETTY,
    print_stderr: PrintStdErr = False,
    print_stdout: PrintStdOut = True,
) -> None:
    options = Options(
        command=command,
        iterations=iterations,
        delay=delay,
        print_stderr=print_stderr,
        print_stdout=print_stdout,
        timeout=timeout,
        output_mode=output,
    )
    try:
        asyncio.run(Cmder.from_options(options).iterate())
    except Exception:
        Console(stderr=True).print_exception(show_locals=True)


if __name__ == "__main__":
    app()
