import microtest
import io
import contextlib
import templateman.cli as cli


path_opened = ''
script_text = ''


class DummyFile:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
    
    def read(self):
        return script_text


def dummy_open(path: str, mode='r', *args, **kwargs) -> DummyFile:
    global path_opened
    path_opened = path
    return DummyFile()


@microtest.reset
def on_reset():
    global path_opened
    path_opened = ''
    script_text = ''


@microtest.test
def test_running_uninstalled_scripts():
    global script_text
    dummy_builtins = cli.__builtins__.copy()
    dummy_builtins['open'] = dummy_open
    script_text = "print('module executed')\n"
    
    with io.StringIO() as stream:
        with contextlib.redirect_stdout(stream):
            with microtest.patch(cli, __builtins__ = dummy_builtins):
                cli.run(['script.py'])
            
            output = stream.getvalue()
            assert 'module executed' in output
            assert 'script.py' in path_opened


@microtest.test
def test_argument_passing():
    global script_text
    dummy_builtins = cli.__builtins__.copy()
    dummy_builtins['open'] = dummy_open
    script_text = '\n'.join([
        'import templateman',
        "print(f\"name = {templateman.template_info.get('name')}\")",
    ])
    
    with io.StringIO() as stream:
        with contextlib.redirect_stdout(stream):
            with microtest.patch(cli, __builtins__ = dummy_builtins):
                cli.run(['script.py', '--name', 'NAME'])
            
            output = stream.getvalue()
            assert 'name = NAME' in output
            assert 'script.py' in path_opened


if __name__ == '__main__':
    microtest.run()
