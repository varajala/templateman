import os
import sys
import shutil
import subprocess as subp
import io
import types


running = False
working_dir: str = os.getcwd()
project_info = {
    'project_name': None,
    'author_name': None,
    'license': None,
}


def print_error(message: str, add_newline = True):
    prefix = '[ ERROR ] '
    sys.stderr.write(prefix)
    sys.stderr.write(message)
    if add_newline:
        sys.stderr.write('\n')


def abort():
    global running
    running = False
    sys.exit(1)


def create_directory(name: str, create_path = False):
    dir_path = os.path.join(working_dir, name)
    try:
        if create_path:
            os.makedirs(dir_path)
        else:
            os.mkdir(dir_path)
    
    except (OSError, PermissionError) as err:
        print_error(str(err))
        abort()


def create_file(name: str):
    filepath = os.path.join(working_dir, name)
    try:
        open(filepath, 'x').close()
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


def run_command(cmd: types.List[str], change_path = '') -> types.Tuple[int, str]:
    path = working_dir
    if change_path:
        path = os.path.abspath(os.path.join(working_dir, path))
    
    stream = io.StringIO()
    proc = subp.run(cmd, cwd=path, stdout=stream, stderr=stream, text=True)
    
    stream.seek(0)
    output = stream.read(),
    stream.close()
    return proc.returncode, output
