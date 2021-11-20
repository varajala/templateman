import sys
import os
import runpy
import typing as types
import templateman


commands: types.Dict[str, types.Callable[[types.List[str],], None]] = dict()


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


@register_command
def help(args: types.List[str]):
    print('HELP')


@register_command
def install(args: types.List[str]):
    print('INSTALL')


@register_command
def run(args: types.List[str]):
    if len(args) < 1:
        templateman.print_error("Command 'run' expected atleast one argument")
        templateman.abort()
        return
    
    filename, suffix = os.path.splitext(args[0])
    filepath = os.path.join(templateman.working_dir, args[0])
    if suffix == '':
        # TODO: search for installed templates
        # filepath = os.path.join(--, filename + '.py')
        pass

    def set_name(args: types.List[str]):
        templateman.template_info['name'] = args[0]

    def set_output_directory(args: types.List[str]):
        templateman.template_info['output_directory'] = args[0]

    all_options = {
        '--name': (1, set_name),
        '-n': (1, set_name),

        '--output-directory': (1, set_output_directory),
        '-o': (1, set_output_directory),
    }
    parse_args(args[1:], all_options)

    with open(filepath, 'r') as file:
        code = file.read()
        try:
            exec(compile(code, filename, 'exec'))
        except Exception as err:
            error_message = 'There were errors during the execution of the script:'
            error_message += f'\n{err.__class__.__name__}: {str(err)}'
            templateman.print_error(error_message)
            templateman.abort()
