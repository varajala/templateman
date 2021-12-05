## templateman.cli

```python
"""
The command line interface implementation.

Author: Valtteri Rajalainen
"""

VERSION: '0.0.1a'
TEMPLATE_DIRECTORY_ENV_VAR: 'PY_TEMPLATES_DIR'
commands: dict()


def mkdir_exc_safe(path: str) -> types.Optional[str]:
  pass

def copy_file_exc_safe(src: str, dst: str) -> types.Optional[str]:
  pass

def list_directory_exc_safe(path: str) -> types.Tuple[types.List[str], types.Optional[str]]:
  pass

def open_file_exc_safe(path: str, mode = 'r', *args) -> types.Tuple[object, types.Optional[str]]:
  pass

def remove_file_exc_safe(path: str) -> types.Optional[str]:
  pass

def register_command(alias: str):
  pass

def exec_command(command: str, args: types.List[str]):
  pass

def parse_args(args: types.List[str], options: dict):
  pass

def resolve_template_directory() -> types.Optional[str]:
  pass

@register_command('help')
def print_help(args: types.List[str]):
  """
  Show this help information.
  """

@register_command('remove')
def remove_installed_template(args: types.List[str]):
  """
  Remove installed template. This will remove the file from the
  template directory permanently.
  
  USAGE:
  
      $ python -m templateman remove [template-name]
  """

@register_command('list')
def list_installed_templates(args: types.List[str]):
  """
  List all installed templates.
  """

@register_command('install')
def install_template(args: types.List[str]):
  """
  Install a template script. This creates a copy of the provided file
  into the template directory.
  
  USAGE:
  
      $ python -m templateman install [filepath]
  """

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

```

