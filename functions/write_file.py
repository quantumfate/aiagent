import os
from functions.helper import is_in_working_dir, write_content_to_file


def write_file(working_directory, file_path, content):
    target_file, valid_target_file = is_in_working_dir(working_directory, file_path)

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(working_directory, exist_ok=True)

    return write_content_to_file(target_file, content)
