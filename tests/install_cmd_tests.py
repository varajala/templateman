import microtest
import io
import contextlib
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
                    cli.install(list())
                    assert mkdir_called == 1
                    
                    cli.install(list())
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
                    cli.install(list())
                    assert directory_exists_check
                    assert directory_created


if __name__ == '__main__':
    microtest.run()
