import asyncio
import sys
from dataclasses import dataclass


@dataclass
class CmdResult:
    cmd: str
    stdout: str | None = None
    stderr: str | None = None
    returncode: int | None = None
    exception: Exception | None = None


async def run_cmd(cmd: str) -> CmdResult:
    print("run_cmd ", cmd)
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    result = CmdResult(cmd=cmd)

    try:
        stdout, stderr = await process.communicate()
        result.stdout = stdout.decode()
        result.stderr = stderr.decode()
        result.returncode = process.returncode
        return result
    except Exception as e:
        process.kill()
        result.exception = e
        return result
    except BaseException as e:
        process.kill()
        raise e


if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:])
    result = asyncio.run(run_cmd(cmd))
    print(f"Command: {result.cmd}")
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    if result.exception:
        print(f"Exception: {result.exception}")
