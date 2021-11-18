import sys
import typing as types
import templateman


commands: types.Dict[str, types.Callable[[types.List[str],], None]] = dict()


def register_command(func: types.Callable[[types.List[str],], None]):
    commands[func.__name__] = func
    return func


@register_command
def help(args: types.List[str]):
    print('HELP')


@register_command
def run(args: types.List[str]):
    print('RUN')


def main(args: types.List[str]) -> int:
    if len(args) < 1:
        help(None)
        return 0
    
    command = args[0]
    if command not in commands:
        templateman.print_error(f"Unknown command '{command}'. Use 'help' to check all commands...")
        return 1
    
    commands[command](args[1:])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
