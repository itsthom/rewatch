import asyncio
import random
import time

from rewatch.models.cmd_result import CmdResult

ARTIFICIAL_LATENCY = 5.00


async def run_cmd(cmd: str, timeout: float) -> CmdResult:
    start = time.perf_counter()
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    result = CmdResult(cmd=cmd)

    try:
        async with asyncio.timeout(timeout):
            if ARTIFICIAL_LATENCY:
                await asyncio.sleep(ARTIFICIAL_LATENCY * random.random())

            stdout, stderr = await process.communicate()
            result.stdout = stdout.decode()
            result.stderr = stderr.decode()
            result.returncode = process.returncode
    except Exception as e:
        result.exception = e
    finally:
        result.elapsed_s = time.perf_counter() - start

    return result
