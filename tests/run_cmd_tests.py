import microtest
import microtest.utils as utils

import io
import os
import contextlib

import templateman.cli as cli


@microtest.test
def test_running_uninstalled_scripts():
    SCRIPT_NAME = 'script.py'
    with utils.create_temp_dir(files=[SCRIPT_NAME]) as script_dir:
        with open(os.path.join(script_dir, SCRIPT_NAME), 'w') as script_file:
            script_file.write("print('module executed')\n")
        
        with io.StringIO() as stream:
            with contextlib.redirect_stdout(stream):
                cli.run([os.path.join(script_dir, SCRIPT_NAME)])
        
            output = stream.getvalue()
            assert 'module executed' in output


@microtest.test
def test_running_installed_scripts():
    SCRIPT_NAME = 'script'
    with utils.create_temp_dir(files=[SCRIPT_NAME]) as template_dir:
        env_dict = { cli.TEMPLATE_DIRECTORY_ENV_VAR: template_dir }
        
        with open(os.path.join(template_dir, SCRIPT_NAME), 'w') as script_file:
            script_file.write("print('module executed')\n")
        
        with microtest.patch(cli.os, environ = env_dict):
            with io.StringIO() as stream:
                with contextlib.redirect_stdout(stream):
                    cli.run([SCRIPT_NAME])
            
                output = stream.getvalue()
                assert 'module executed' in output


@microtest.test
def test_argument_passing():
    SCRIPT_NAME = 'script.py'
    SCRIPT_TEXT = '\n'.join([
        'import templateman',
        "print(f\"name = {templateman.template_info.get('name')}\")",
    ])
    
    with utils.create_temp_dir(files=[SCRIPT_NAME]) as script_dir:
        SCRIPT_PATH = os.path.join(script_dir, SCRIPT_NAME)
        with open(SCRIPT_PATH, 'w') as script_file:
            script_file.write(SCRIPT_TEXT)
        
        with io.StringIO() as stream:
            with contextlib.redirect_stdout(stream):
                cli.run([SCRIPT_PATH, '--name', 'NAME'])
        
            output = stream.getvalue()
            assert 'name = NAME' in output


@microtest.test
def test_running_non_existent_scripts():
    SCRIPT_NAME = 'script.py'
    with io.StringIO() as stream:
        with contextlib.redirect_stderr(stream):
            cli.run([SCRIPT_NAME])
            output = stream.getvalue()
            assert "can't find file" in output.lower()


@microtest.test
def test_running_scripts_with_restricted_permissions():
    SCRIPT_NAME = 'script.py'
    with utils.create_temp_dir(files=[SCRIPT_NAME]) as script_dir:
        SCRIPT_PATH = os.path.join(script_dir, SCRIPT_NAME)
        with utils.set_as_unauthorized(SCRIPT_PATH):
            with io.StringIO() as stream:
                with contextlib.redirect_stderr(stream):
                    cli.run([SCRIPT_PATH])
                output = stream.getvalue()
                assert "can't open file" in output.lower()


if __name__ == '__main__':
    microtest.run()
