"""
Main entrypoint for the cli.

Author: Valtteri Rajalainen
"""

import sys
import typing as types

import templateman
import templateman.cli as cli


def main(args: types.List[str]) -> int:
    if len(args) < 1:
        cli.print_help(None)
        return 0
    
    command = args[0]
    if command not in cli.commands:
        templateman.print_error(f"Unknown command '{command}'. Use 'help' to check all commands...")
        return 1
    
    templateman.running = True
    cli.exec_command(command, args[1:])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
