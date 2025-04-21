from rewatch.cmder.abc import CmderAbc
from rewatch.cmder.bars import CmderBars
from rewatch.cmder.dots import CmderDots
from rewatch.cmder.json import CmderJson
from rewatch.cmder.no_output import CmderNoOutput
from rewatch.cmder.pretty import CmderPretty
from rewatch.cmder.raw import CmderRaw
from rewatch.models.options import Options
from rewatch.models.output_mode import OutputMode


class Cmder:
    @staticmethod
    def from_options(options: Options) -> CmderAbc:
        if options.output_mode == OutputMode.BARS:
            return CmderBars(options)
        if options.output_mode == OutputMode.DOTS:
            return CmderDots(options)
        if options.output_mode == OutputMode.JSON:
            return CmderJson(options)
        if options.output_mode == OutputMode.NONE:
            return CmderNoOutput(options)
        if options.output_mode == OutputMode.PRETTY:
            return CmderPretty(options)
        if options.output_mode == OutputMode.RAW:
            return CmderRaw(options)

        raise ValueError(f"Unknown output mode: {options.output_mode}")
