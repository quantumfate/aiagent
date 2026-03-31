import os
from functions.helper import is_in_working_dir, read_n_chars_from_file


def get_files_info(working_directory, directory="."):
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
