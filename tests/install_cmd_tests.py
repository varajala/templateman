import io
import os
import contextlib
import tempfile
import microtest
import microtest.utils as utils
import templateman.cli as cli


@microtest.test
def test_template_directory_creating():
    mkdir_called = 0

    def dummy_mkdir(*args):
        nonlocal mkdir_called
        mkdir_called += 1

    def dummy_path_exists(*args):
        return mkdir_called > 0

    with io.StringIO() as stream:
        with contextlib.redirect_stderr(stream):
            with microtest.patch(cli.os, mkdir = dummy_mkdir):
                with microtest.patch(cli.os.path, exists = dummy_path_exists):
                    cli.install_template(list())
                    assert mkdir_called == 1
                    
                    cli.install_template(list())
                    assert mkdir_called == 1


@microtest.test
def test_template_directory_config():
    directory_exists_check = False
    directory_created = False
    dir_path = 'some-directory'
    env_dict = { cli.TEMPLATE_DIRECTORY_ENV_VAR: dir_path }

    def dummy_path_exists(path):
        nonlocal directory_exists_check
        if path == dir_path:
            directory_exists_check = True
        return False

    def dummy_mkdir(path):
        nonlocal directory_created
        if path == dir_path:
            directory_created = True
    
    with io.StringIO() as stream:
        with contextlib.redirect_stderr(stream):
            with microtest.patch(cli.os, environ = env_dict, mkdir = dummy_mkdir):
                with microtest.patch(cli.os.path, exists = dummy_path_exists):
                    cli.install_template(list())
                    assert directory_exists_check
                    assert directory_created


@microtest.test
def test_valid_install():
    with utils.create_temp_dir() as templates_path:
        env_dict = { cli.TEMPLATE_DIRECTORY_ENV_VAR: templates_path }
        with tempfile.NamedTemporaryFile(suffix='.py') as script_file:
            with microtest.patch(os, environ = env_dict):
                cli.install_template([script_file.name])
                templates = os.listdir(templates_path)
                
                _, filename = os.path.split(script_file.name)
                filename, _ = os.path.splitext(filename)
                assert filename in templates


@microtest.test
def test_install_non_existing_file():
    with io.StringIO() as stream:
        with contextlib.redirect_stderr(stream):
            with utils.create_temp_dir() as templates_path:
                env_dict = { cli.TEMPLATE_DIRECTORY_ENV_VAR: templates_path }
                with microtest.patch(os, environ = env_dict):
                    cli.install_template(['script.py'])
                    output = stream.getvalue()
                    assert 'path does not exist' in output.lower()


@microtest.test
def test_error_handling_when_user_home_directory_cant_be_resolved():
    def raise_exception(*args):
        raise Exception
    
    with microtest.patch(cli.os.path, expanduser = raise_exception):
        path = cli.resolve_template_directory()
        assert path is None
    


if __name__ == '__main__':
    microtest.run()
