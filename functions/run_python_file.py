from ast import arg
import os
import subprocess
from typing import Iterable
from functions.helper import is_in_working_dir
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file with specified arguments if and only if it's relative to the current working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the python file to be executed and relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments parsed to the python file",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)


def __build_output(abritary_process: subprocess.CompletedProcess[str]) -> str:
    """Aggregates a string with a STDERR and STDOUT stream of a given process

    Args:
        abritary_process (subprocess.CompletedProcess[str]): The completed process

    Returns:
        The context of a completed process
    """
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
) -> str:
    """Runs a specified python file with specified arguments if and only if it's relative to the current working directory

    Args:
        working_directory (str): The current working directory
        file_path (str): File path of the python file to be executed and relative to the working directory (default is the working directory itself)
        args: The arguments parsed to the python file

    Returns:
        STDOUT and STDERR of the executed python file or a string describing no output
    """
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
