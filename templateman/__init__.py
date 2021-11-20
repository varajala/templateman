"""
Utilities for creating template scripts.

Author: Valtteri Rajalainen
"""

import os
import sys
import shutil
import subprocess as subp
import tempfile
import typing as types


running = False
working_dir: str = os.getcwd()
template_info: types.Dict[str, types.Optional[str]] = {
    'name':             'UNKNOWN',
    'output_directory': working_dir,
    'author':           'UNKNOWN',
}


def require_arguments(*args):
    for arg in args:
        if template_info.get(arg) == 'UNKNOWN':
            print_error(f"Missing required argument '{arg}'")
            abort()


def print_error(message: str, add_newline = True):
    prefix = '[ ERROR ] '
    sys.stderr.write(prefix)
    sys.stderr.write(message)
    if add_newline:
        sys.stderr.write('\n')


def abort():
    global running
    if running:
        running = False
        sys.exit(1)


def create_directory(path: str, create_dirs = False):
    try:
        if create_dirs:
            os.makedirs(path)
        else:
            os.mkdir(path)
    
    except (OSError, PermissionError) as err:
        print_error(str(err))
        abort()


def create_file(path: str):
    try:
        open(path, 'x').close()
    except (OSError, PermissionError) as err:
        print_error(str(err))
        abort()


def copy_item(src: str, dst: str):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)

    except (OSError, PermissionError) as err:
        print_error(str(err))
        abort()


def run_command(cmd: types.List[str], path = working_dir) -> types.Tuple[int, str]:
    with tempfile.TemporaryFile(mode='w+') as file:
        proc = subp.run(cmd, cwd=path, stdout=file, stderr=file, text=True)
        file.seek(0)
        return proc.returncode, file.read()

