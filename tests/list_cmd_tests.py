import microtest
import microtest.utils as utils

import os
import io
import contextlib
import templateman.cli as cli


@microtest.test
def test_template_listing():
    INSTALLED_TEMPLATES = ['template_1', 'template_2']
    with io.StringIO() as stream:
        with utils.create_temp_dir(files=INSTALLED_TEMPLATES) as dir_path:
            env_dict = { cli.TEMPLATE_DIRECTORY_ENV_VAR: dir_path }
            with microtest.patch(cli.os, environ=env_dict):
                with contextlib.redirect_stdout(stream):
                    cli.list_installed_scripts(list())
            output = stream.getvalue()
            assert 'template_1' in output
            assert 'template_2' in output


if __name__ == '__main__':
    microtest.run()
