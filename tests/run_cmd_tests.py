import microtest
import io
import contextlib
import templateman.cli as cli


path_opened = ''


class DummyFile:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
    
    def read(self):
        return "print('module executed')\n"


def dummy_open(path: str, mode='r', *args, **kwargs) -> DummyFile:
    global path_opened
    path_opened = path
    return DummyFile()


@microtest.test
def test_running_scripts():
    dummy_builtins = cli.__builtins__.copy()
    dummy_builtins['open'] = dummy_open
    
    with io.StringIO() as stream:
        with contextlib.redirect_stdout(stream):
            with microtest.patch(cli, __builtins__ = dummy_builtins):
                cli.run(['script.py'])
            
            output = stream.getvalue()
            assert 'module executed' in output
            assert 'script.py' in path_opened


if __name__ == '__main__':
    microtest.run()
