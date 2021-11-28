import microtest
import microtest.utils as utils

import os
import contextlib
import templateman.cli as cli


@microtest.test
def test_removing_templates():
    def dummy_input(*args):
        return 'Y'

    dummy_builtins = cli.__builtins__.copy()
    dummy_builtins['input'] = dummy_input

    with open(os.devnull, 'w') as DEVNULL:
        with utils.create_temp_dir(files=['template']) as dir_path:
            TEMPLATE_PATH = os.path.join(dir_path, 'template')
            env_dict = { cli.TEMPLATE_DIRECTORY_ENV_VAR: dir_path }
            with microtest.patch(cli, __builtins__=dummy_builtins):
                with microtest.patch(cli.os, environ=env_dict):
                    with contextlib.redirect_stdout(DEVNULL):
                        cli.remove_installed_template(['template'])
            assert not os.path.exists(TEMPLATE_PATH)


if __name__ == '__main__':
    microtest.run()
