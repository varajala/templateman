# Examples

## Table of contents

  - [Creating scripts](#creating-scripts)
  - [Running scripts](#running-scripts)
  - [Managing scripts](#managing-scripts)


## Creating scripts

Let's create a simple script for automating C header file creation. We would like the script to create a new file into the specified directory, with a specified name. The file should contain the follofing lines:

```c
#ifndef FILENAME_H
#define FILENAME_H


#endif
```

Templateman simply executes Python modules that contain arbitrary code. Here's a script that creates a file with the previously described C header file format:

```python
import os
import templateman

# Abort if no --name flag is given
templateman.require_arguments('name')

# Fetch the filename and write text into the file
name = templateman.template_info['name']
filename = name + '.h'
filepath = os.path.join(
    templateman.template_info['output_directory'],
    filename
    )

lines = '\n'.join([
    f'#ifndef {name.upper()}_H',
    f'#define {name.upper()}_H',
    '',
    '',
    '#endif',
    ''
])

with open(filepath, 'w') as file:
    file.write(lines)

```

First we import os for the os.path module and templateman, that provides the information provided by the user via the CLI. These arguments can be accessed trough the **templateman.template_info** - dictionary.

After the import statements, we tell templateman that this script requires the *name* argument from the user to function correctly. This is doen with the **templateman.require_arguments** - function. This will aboert the script execution and print an error message to the user if any required arguments are missing.

After this we write the contents into a new file, as usually in Python.


## Running scripts

To execute scripts use the **run** - command.

    python -m templateman run script.py

The **run** - command expects a filepath or a name as an argument. If the path or name provided does not contain any suffix (.py, .txt, .js, etc...), templateman will search a specific template directory for the script. If the path has any suffix, it will search the filesystem with the provided path relative from the current directory. If the filepath is absolute, it will be used instead.


> **NOTE**: Don't execute scripts you don't trust, or know exactly what they do!


## Managing scripts

Templateman can copy scripts into a single directory, so you don't have to remember the paths to each script you create. For this, use the **install** - command.

    python -m templateman install script.py

This will copy the file into a directory, which templateman knows to search by default. By default the directory is called **.py-templates** and it is created into user's home directory. You can change this by setting an environment variable called **PY_TEMPLATES_DIR** to point to the desired directory.

To check installed scripts, use the **list** - command.

    python - m templateman list

This command will list out all files inside the template directory. You can also see the directory path templateman searches for installed templates.

To remove installed script use the **remove** - command. This will remove the file from the template directory permanently.

    python -m templateman remove script
