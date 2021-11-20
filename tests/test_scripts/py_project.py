"""
A templateman script for creating a simple Python project.

    [project-name]
    |
    | - [project-name]
    |   |
    |   . __init__.py
    |   . __main__.py
    |
    | - tests
    |   |
    |
    . .gitignore
    . setup.py


Executing "python -m [project-name]" should output
"hello, World!" if script ran succesfully.

Author: Valtteri Rajalainen
"""

import os
import sys
import templateman

# Abort if no --name flag is given
templateman.require_arguments('name')

name = templateman.template_info['name']
root_path = os.path.join(templateman.template_info['output_directory'], name)
src_directory = os.path.join(root_path, name)
tests_directory = os.path.join(root_path, 'tests')

templateman.create_directory(root_path)
templateman.create_directory(src_directory)
templateman.create_directory(tests_directory)

gitignore_text = """# __pycache__
**/__pycache__
**.pyc

# mypy-cache
.mypy_cache

# virtual environment
*env

"""
with open(os.path.join(root_path, '.gitignore'), 'w') as gitignore:
    gitignore.write(gitignore_text)


py_setup_text = f"""from setuptools import find_packages, setup


setup(
    name='{name}',
    version='0.0.1a',
    author='{templateman.template_info['author']}',
    python_requires='>=3.7',
    packages=find_packages(),
)

"""
with open(os.path.join(root_path, 'setup.py'), 'w') as py_setup:
    py_setup.write(py_setup_text)


create_venv_command = [sys.executable, '-m', 'venv', 'venv']
templateman.run_command(create_venv_command, path=root_path)

_, py_interpreter_file = os.path.split(sys.executable)
py_venv_interpreter_path = os.path.abspath(os.path.join(root_path, 'venv/bin/' + py_interpreter_file))
install_project_command = [py_venv_interpreter_path, '-m', 'pip', 'install', '-e', root_path]
templateman.run_command(install_project_command, path=root_path)

templateman.create_file(os.path.join(src_directory, '__init__.py'))

py_main_text = f"""import sys
import typing


def main(args: typing.List[str]) -> int:
    print("Hello, World!")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

"""
with open(os.path.join(src_directory, '__main__.py'), 'w') as py_main:
    py_main.write(py_main_text)
