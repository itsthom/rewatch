import asyncio
import dataclasses

from rich.console import Console
from rich.pretty import Pretty
from typer import Typer

from rewatch.cmder import run_cmd

app = Typer(rich_markup_mode="rich")


@app.command(context_settings={"ignore_unknown_options": True})
def main(args: list[str]) -> None:
    try:
        result = asyncio.run(run_cmd(" ".join(args)))
        pretty = Pretty(dataclasses.asdict(result), expand_all=True)
        Console().print(pretty)
    except Exception:
        Console(stderr=True).print_exception(show_locals=True)


if __name__ == "__main__":
    app()
