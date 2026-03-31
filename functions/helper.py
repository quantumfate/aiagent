import os
import sys

from config import MAX_CHARS


def is_valid_target(working_directory: str, file: str = ".") -> tuple[str, bool]:
    """Constructs an absolute path from {working_directory} and {file}

    Args:
        working_directory: the path to the working directory
        file: the name of a directory or a file within the {working_directory}

    Returns:
        - target
        - wether tagert is within {working_directory}
    """
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, file))

    return target, os.path.commonpath([working_dir_abs, target]) == working_dir_abs


def read_file(file_path: str) -> str:
    """Reads up to {MAX_CHARS} characters from a given file

    Args:
        file_path (str): The absolute path to a file

    Returns:
        The contents of the file

    Raises:
        OSError: Re-throw with additional information
    """
    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string

    except OSError as e:
        raise OSError(f"Failed to read {file_path}: {e}") from e
