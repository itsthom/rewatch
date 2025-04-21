from dataclasses import dataclass

from rewatch.models.output_mode import OutputMode


@dataclass(frozen=True)
class Options:
    # Command Options
    command: list[str]
    delay: float
    iterations: int
    timeout: float
    # Output Options
    output_mode: OutputMode
    print_stderr: bool
    print_stdout: bool
