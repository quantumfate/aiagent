import os
from google.genai import types
from functions.helper import is_in_working_dir, read_n_chars_from_file

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """Lists files in a specified directory relative to the working directory, providing file size and directory status

    Args:
        working_directory (str): working directory of the agent
        directory (str): specified directory

    Returns:
        A formatted and joined string of the files
    """
    target_dir, in_working_dir = is_in_working_dir(working_directory, directory)

    if not in_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    file_stats = ()
    for file_name in os.listdir(target_dir):
        full_path = os.path.normpath(os.path.join(target_dir, file_name))
        file_stats += (
            f"- {file_name}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}",
        )

    return "\n".join(file_stats)
