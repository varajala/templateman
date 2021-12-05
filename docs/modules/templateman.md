## templateman

```python
"""
Utilities for creating template scripts.

Author: Valtteri Rajalainen
"""

running: False
working_dir: str = None
template_info: {'name': 'UNKNOWN', 'output_directory': working_dir, 'author': 'UNKNOWN'}


def require_arguments(*args):
  pass

def print_error(message: str, add_newline = True):
  pass

def abort():
  pass

def create_directory(path: str, create_dirs = False):
  pass

def create_file(path: str):
  pass

def copy_item(src: str, dst: str):
  pass

def run_command(cmd: types.List[str], path = working_dir) -> types.Tuple[int, str]:
  pass

```

