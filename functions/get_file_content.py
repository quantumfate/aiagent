import os
from functions.helper import is_valid_target, read_n_chars_from_file


def get_file_content(working_directory, file_path):
    target_file, valid_file = is_valid_target(working_directory, file_path)

    if not valid_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    return read_n_chars_from_file(target_file)
