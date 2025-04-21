from typing import Annotated

from typer import Argument, BadParameter, Context, Option

from rewatch.models.output_mode import OutputMode


def validate_delay(ctx: Context, value: float) -> float | None:
    return _validate_non_negative_float("Delay", ctx, value)


def validate_iterations(ctx: Context, value: int) -> int | None:
    if ctx.resilient_parsing:
        return None
    if value < 1:
        raise BadParameter(f"Iterations must be positive (received {value})")
    return value


def validate_timeout(ctx: Context, value: float) -> float | None:
    return _validate_non_negative_float("Timeout", ctx, value)


def _validate_non_negative_float(
    param: str, ctx: Context, value: float
) -> float | None:
    if ctx.resilient_parsing:
        return None
    if value < 0:
        raise BadParameter(f"{param} must not be negative (received {value})")
    return value


Command = Annotated[list[str], Argument(help="Shell command to run.")]

Delay = Annotated[
    float,
    Option(
        "--rw-delay",
        callback=validate_delay,
        help="Delay between commands in seconds.",
        rich_help_panel="Command Options",
    ),
]

Iterations = Annotated[
    int,
    Argument(
        callback=validate_iterations,
        help="Number of iterations to run.",
    ),
]

Output = Annotated[
    OutputMode,
    Option(
        "--rw-output",
        help="Output mode for command results.",
        rich_help_panel="Output Options",
    ),
]

PrintStdErr = Annotated[
    bool,
    Option(
        "--rw-stderr/--no-rw-stderr",
        help="If output mode prints output, include captured stderr.",
        rich_help_panel="Output Options",
    ),
]

PrintStdOut = Annotated[
    bool,
    Option(
        "--rw-stdout/--no-rw-stdout",
        help="If output mode prints output, include captured stdout.",
        rich_help_panel="Output Options",
    ),
]

Timeout = Annotated[
    float,
    Option(
        "--rw-timeout",
        help="Timeout for each command in seconds.",
        rich_help_panel="Command Options",
    ),
]
