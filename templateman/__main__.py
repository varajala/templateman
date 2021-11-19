import sys
import os
import runpy
import typing as types
import templateman


commands: types.Dict[str, types.Callable[[types.List[str],], None]] = dict()


def register_command(func: types.Callable[[types.List[str],], None]):
    commands[func.__name__] = func
    return func


def parse_args(args: types.List[str], options: dict):
    skip = -1
    for i in range(0, len(args)):
        if skip > i:
            continue
        
        arg = args[i]
        if arg not in options:
            templateman.print_error(f"Unknown option '{arg}'")
            templateman.abort()
        
        args_consumed, handle_options = options[arg]
        start = i + 1
        end = start + args_consumed
        if len(args) < end:
            templateman.print_error(f"Option '{arg}' expected additional arguments")
            templateman.abort()
        
        handle_options(args[start:end])
        skip = end


@register_command
def help(args: types.List[str]):
    print('HELP')


@register_command
def run(args: types.List[str]):
    if len(args) < 1:
        templateman.print_error("Command 'run' expected atleast one argument")
        templateman.abort()
    
    script_name = args[0]
    filepath = os.path.join(templateman.working_dir, script_name)
    if not os.path.exists(filepath) or not os.path.isfile(filepath) or not os.path.splitext(filepath)[1] == '.py':
        templateman.print_error(f"Path '{filepath}' does not exist or it is not a Python module")
        templateman.abort()

    def set_name(args: types.List[str]):
        templateman.template_info['name'] = args[0]

    all_options = {
        '--name': (1, set_name),
        '-n': (1, set_name),
    }
    parse_args(args[1:], all_options)

    with open(filepath, 'r') as file:
        code = file.read()

        try:
            exec(compile(code, script_name, 'exec'))
        except Exception as err:
            templateman.print_error(f'There were errors during the execution of the script:\n{err.__class__.__name__}: {str(err)}')
            templateman.abort()


def main(args: types.List[str]) -> int:
    if len(args) < 1:
        help(None)
        return 0
    
    command = args[0]
    if command not in commands:
        templateman.print_error(f"Unknown command '{command}'. Use 'help' to check all commands...")
        return 1
    
    templateman.running = True
    commands[command](args[1:])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
