import os
import templateman

# Abort if no --name flag is given
templateman.require_arguments('name')

# Fetch the filename and write text into the file
name = templateman.template_info['name']
filename = name + '.h'
filepath = os.path.join(templateman.template_info['output_directory'], filename)

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
