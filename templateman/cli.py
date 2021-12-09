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

VERSION = '1.0.0'
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


def open_file_exc_safe(path: str, mode = 'r', *args) -> types.Tuple[object, types.Optional[str]]:
    file = None
    error = None
    try:
        file = open(path, mode, *args)
    except Exception as err:
        error = f"{err.__class__.__name__}: {str(err)}"
    return file, error


def remove_file_exc_safe(path: str) -> types.Optional[str]:
    try:
        os.remove(path)
        return None
    except (OSError, PermissionError) as err:
        return str(err)


def register_command(alias: str):
    def wrapper(func: types.Callable[[types.List[str],], None]):
        commands[alias] = func
        return func
    return wrapper


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


@register_command('help')
def print_help(args: types.List[str]):
    """Show this help information."""
    def format_command_info(name: str, docstring: str = None) -> str:
        if docstring is None:
            return '  > ' + name + ': ' + 'No description available...\n'
        return '  > ' + name + ': ' + docstring.strip() + '\n'

    commands_help = [format_command_info(name, func.__doc__) for name, func in commands.items()]
    help_text = [
        f'TemplateManager, version: {VERSION}',
        '',
        'A simple utility to manage and run Python scripts for automating',
        'project creation, boilerplate code and much more.'
        '',
        'Usage: ',
        '',
        '   $ python -m templateman [command] [arguments]',
        '',
        '',
        'Implemented commands:',
        '',
        *commands_help,
    ]
    print('\n'.join(help_text))


@register_command('remove')
def remove_installed_template(args: types.List[str]):
    """
    Remove installed template. This will remove the file from the
    template directory permanently.

    USAGE:
    
        $ python -m templateman remove [template-name]

    """
    template_dir = resolve_template_directory()
    if template_dir is None:
        error_message = 'Can\'t resolve users home directory for storing template scripts'
        templateman.print_error(error_message)
        templateman.abort()
        return

    if len(args) == 0:
        templateman.print_error("Command 'remove' expected atleast one argument")
        templateman.abort()
        return

    template_path = os.path.join(template_dir, args[0])
    if not os.path.exists(template_path):
        templateman.print_error(f"No template installed with name '{args[0]}'")
        templateman.abort()
        return

    print(f"Are you sure you want to remove file '{template_path}' premanently?")
    ans = input('Input Y/y to remove this file: ')
    if ans.lower() == 'y':
        error = remove_file_exc_safe(template_path)
        if error:
            error_message = 'Unexpected error when removing file:\n'
            error_message += error
            templateman.print_error(error_message)
            templateman.abort()
            return


@register_command('list')
def list_installed_templates(args: types.List[str]):
    """List all installed templates."""
    template_dir = resolve_template_directory()
    if template_dir is None:
        error_message = 'Can\'t resolve users home directory for storing template scripts'
        templateman.print_error(error_message)
        templateman.abort()
        return

    if not os.path.exists(template_dir):
        error = mkdir_exc_safe(template_dir)
        if error:
            error_message = 'Failed to create directory for storing template scripts:\n'
            error_message += error
            templateman.print_error(error_message)
            templateman.abort()
            return

    installed_templates, error = list_directory_exc_safe(template_dir)
    if error:
        error_message = 'Unexpected error when listing installed templates:\n'
        error_message += error
        templateman.print_error(error_message)
        templateman.abort()
        return

    print('Templates stored in directory:')
    print(template_dir)
    print()
    for template_name in installed_templates:
        print('> ', template_name)
    if installed_templates:
        print()


@register_command('install')
def install_template(args: types.List[str]):
    """
    Install a template script. This creates a copy of the provided file
    into the template directory.

    USAGE:

        $ python -m templateman install [filepath]
    
    """
    template_dir = resolve_template_directory()
    if template_dir is None:
        error_message = 'Can\'t resolve users home directory for storing template scripts'
        templateman.print_error(error_message)
        templateman.abort()
        return
    
    if not os.path.exists(template_dir):
        error = mkdir_exc_safe(template_dir)
        if error:
            error_message = 'Failed to create directory for storing template scripts:\n'
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

    error = copy_file_exc_safe(filepath, os.path.join(template_dir, filename))
    if error:
        error_message = 'Install failed:\n'
        error_message += error
        templateman.print_error(error_message)
        templateman.abort()
        return


@register_command('run')
def run_template(args: types.List[str]):
    """
    Execute a template script. If the given filepath has no suffix, an installed
    template is searched. If file has any suffix, the current working directory is
    searched.

    USAGE:

        $ python -m templateman run [template-name] [arguments]

    ARGUMENTS:
        -o / --output-directory: Provide a output directory path for the script.
                                 Default value is the current working directory.

        -n / --name: Provide a name for the script. This should be used to name
                     the generated file, project or other assets.
                     Default value is "UNKNOWN".

        -a / --author: Provide author name for the script. This should be used
                       in config/setup files in place of project's author name.
                       Default value is "UNKNOWN".

    """
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
