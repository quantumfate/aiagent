import os
from google.genai import types
from functions.helper import is_in_working_dir, read_n_chars_from_file

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the current working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read the content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    """Reads the content of a specified file relative to the current working directory.

    Args:
        working_directory (str): working directory of the agent
        file_path (str): file to read from

    Returns:
        The content of the file
    """
    target_file, in_working_dir = is_in_working_dir(working_directory, file_path)

    if not in_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    return read_n_chars_from_file(target_file)
