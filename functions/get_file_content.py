import os
from functions.helper import is_in_working_dir, read_n_chars_from_file


def get_file_content(working_directory, file_path):
    target_file, in_working_dir = is_in_working_dir(working_directory, file_path)

    if not in_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    return read_n_chars_from_file(target_file)
