"""
The command line interface implementation.

Author: Valtteri Rajalainen
"""

import sys
import os
import shutil
import runpy
import contextlib
import typing as types
import templateman


TEMPLATE_DIRECTORY_ENV_VAR = 'PY_TEMPLATES_DIR'

commands: types.Dict[str, types.Callable[[types.List[str],], None]] = dict()


def mkdir_exc_safe(path: str) -> types.Optional[str]:
    error = None
    try:
        os.mkdir(path)
    except Exception as err:
        error = f"{err.__class__.__name__}: {str(err)}"
    return error


def copy_file_exc_safe(src: str, dst: str) -> types.Optional[str]:
    error = None
    try:
        shutil.copy(src, dst)
    except Exception as err:
        error = f"{err.__class__.__name__}: {str(err)}"
    return error


def list_directory_exc_safe(path: str) -> types.Tuple[types.List[str], types.Optional[str]]:
    error = None
    items = list()
    try:
        items = os.listdir(path)
    except Exception as err:
        error = f"{err.__class__.__name__}: {str(err)}"
    return items, error


def open_file_exc_safe(path: str, mode = 'r', *args) -> types.Tuple[types.Optional[types.IO], types.Optional[str]]:
    file = None
    error = None
    try:
        file = open(path, mode, *args)
    except Exception as err:
        error = f"{err.__class__.__name__}: {str(err)}"
    return file, error


def register_command(func: types.Callable[[types.List[str],], None]):
    commands[func.__name__] = func
    return func


def exec_command(command: str, args: types.List[str]):
    if command not in commands:
        raise RuntimeError(f"Unknown comman '{command}'")
    commands[command](args)


def parse_args(args: types.List[str], options: dict):
    skip = -1
    for i in range(0, len(args)):
        if skip > i:
            continue
        
        arg = args[i]
        if arg not in options:
            templateman.print_error(f"Unknown option '{arg}'")
            templateman.abort()
            return
        
        args_consumed, handle_options = options[arg]
        start = i + 1
        end = start + args_consumed
        if len(args) < end:
            templateman.print_error(f"Option '{arg}' expected additional arguments")
            templateman.abort()
            return
        
        handle_options(args[start:end])
        skip = end


def resolve_template_directory() -> types.Optional[str]:
    path = None
    with contextlib.suppress(Exception):
        default_directory = os.path.join(os.path.expanduser('~'), '.py-templates')
        path =  os.environ.get(TEMPLATE_DIRECTORY_ENV_VAR, default_directory)
    return path


@register_command
def help(args: types.List[str]):
    print('HELP')


@register_command
def install(args: types.List[str]):
    template_dir = resolve_template_directory()
    if template_dir is None:
        error_message = 'Can\'t resolve users home directory for storing template scripts'
        templateman.print_error(error_message)
        templateman.abort()
        return
    
    if not os.path.exists(template_dir):
        error = mkdir_exc_safe(template_dir)
        if error:
            error_message = 'Failed to create directory for storing template scripts:'
            error_message += error
            templateman.print_error(error_message)
            templateman.abort()
            return
    
    if len(args) < 1:
        templateman.print_error("Command 'install' expected atleast one argument")
        templateman.abort()
        return

    filepath = args[0]
    if not os.path.isabs(filepath):
        filepath = os.path.join(templateman.working_dir, filepath)
    
    if not os.path.exists(filepath):
        templateman.print_error("Given path does not exist")
        templateman.abort()
        return

    _, filename = os.path.split(filepath)
    filename, _ = os.path.splitext(filename)

    # TODO: verify that the file is Python code

    error = copy_file_exc_safe(filepath, os.path.join(template_dir, filename))
    if error:
        error_message = 'Install failed:\n'
        error_message += error
        templateman.print_error(error_message)
        templateman.abort()
        return


@register_command
def run(args: types.List[str]):
    if len(args) < 1:
        templateman.print_error("Command 'run' expected atleast one argument")
        templateman.abort()
        return
    
    filename, suffix = os.path.splitext(args[0])
    filepath = os.path.join(templateman.working_dir, args[0])
    
    if suffix == '':
        template_dir = resolve_template_directory()
        if template_dir is None:
            error_message = 'Can\'t resolve users home directory for storing template scripts'
            templateman.print_error(error_message)
            templateman.abort()
            return
        
        installed_templates, error = list_directory_exc_safe(template_dir)
        if not error and filename in installed_templates:
            filepath = os.path.join(template_dir, filename)

    def set_name(args: types.List[str]):
        templateman.template_info['name'] = args[0]

    def set_author(args: types.List[str]):
        templateman.template_info['author'] = args[0]

    def set_output_directory(args: types.List[str]):
        templateman.template_info['output_directory'] = args[0]

    all_options = {
        '--name': (1, set_name),
        '-n': (1, set_name),

        '--author': (1, set_author),
        '-a': (1, set_author),

        '--output-directory': (1, set_output_directory),
        '-o': (1, set_output_directory),
    }
    parse_args(args[1:], all_options)

    if not os.path.exists(filepath):
        error_message = f"Can't find file '{filepath}'"
        templateman.print_error(error_message)
        templateman.abort()
        return

    file, error = open_file_exc_safe(filepath, 'r')
    if error:
        error_message = f"Can't open file '{filepath}'"
        templateman.print_error(error_message)
        templateman.abort()
        return

    try:
        code = file.read() # type: ignore
        exec(compile(code, filename, 'exec'))
    
    except Exception as err:
        error_message = 'There were errors during the execution of the script:'
        error_message += f'\n{err.__class__.__name__}: {str(err)}'
        templateman.print_error(error_message)
        templateman.abort()
    
    finally:
        file.close() # type: ignore
