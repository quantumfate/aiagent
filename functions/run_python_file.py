from ast import arg
import os
import subprocess
from typing import Iterable
from functions.helper import is_in_working_dir


def __build_output(abritary_process):
    output = ""

    if abritary_process.returncode != 0:
        output += f"Process exited with code {abritary_process.returncode}\n\n"

    stdout_len = len(abritary_process.stdout)
    stderr_len = len(abritary_process.stderr)

    if max(stdout_len, stderr_len) == 0:
        output += "No output produced\n\n"
    else:
        if stderr_len != 0:
            output += f"STDERR: {abritary_process.stderr}\n\n"
        if stdout_len != 0:
            output += f"STDOUT: {abritary_process.stdout}\n\n"
    return output


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
):
    absolute_file_path, in_working_dir = is_in_working_dir(working_directory, file_path)

    if not in_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", absolute_file_path]

    if args != None:
        command.extend(args)

    abritary_process = subprocess.run(
        command, cwd=working_directory, capture_output=True, text=True, timeout=30.0
    )

    return __build_output(abritary_process)
