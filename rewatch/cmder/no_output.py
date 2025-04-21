from typing import override

from rewatch.cmder.abc import CmderAbc
from rewatch.models.cmd_result import CmdResult


class CmderNoOutput(CmderAbc):
    @override
    def print_cmd_result(self, _result: CmdResult) -> None:
        pass
