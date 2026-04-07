import os
from google.genai import types
from functions.helper import is_in_working_dir, write_content_to_file

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a specified content to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to be written to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Takes a given content and writes it to a specified file

    Args:
        working_directory (str): The working directory
        file_path (str): the file path to write to
        content (str): the content to be written

    Returns:
        A success message describing the operation
    """
    target_file, valid_target_file = is_in_working_dir(working_directory, file_path)

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(working_directory, exist_ok=True)

    return write_content_to_file(target_file, content)
