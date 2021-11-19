import os
import templateman

# Abort if no --name flag is given
templateman.require_arguments('name')

# Fetch the filename and write text into the file
NAME = templateman.template_info['name']
FILENAME = NAME + '.h'
templateman.create_file(FILENAME)

lines = '\n'.join([
    f'#ifndef {NAME.upper()}_H',
    f'#define {NAME.upper()}_H',
    '',
    '',
    '#endif',
    ''
])

with open(os.path.join(templateman.working_dir, FILENAME), 'w') as file:
    file.write(lines)
