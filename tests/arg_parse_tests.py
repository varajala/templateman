import microtest
import contextlib
import io

from templateman.__main__ import parse_args


@microtest.test
def test_arg_parse_valid_command():
    options_set = [None, None, None]
    
    def set_option(index: int, *args):
        options_set[index] = args
    
    options = {
        'option1': (0, lambda args: set_option(0, *args)),
        'option2': (1, lambda args: set_option(1, *args)),
        'option3': (2, lambda args: set_option(2, *args)),
    }

    cli_arguments = ['option1', 'option2', '2', 'option3', '3', '3']
    parse_args(cli_arguments, options)

    assert options_set[0] == tuple()
    assert options_set[1] == ('2',)
    assert options_set[2] == ('3', '3')

    # reset and test  with different order
    options_set = [None, None, None]
    cli_arguments = ['option3', '3', '3', 'option1', 'option2', '2']
    parse_args(cli_arguments, options)

    assert options_set[0] == tuple()
    assert options_set[1] == ('2',)
    assert options_set[2] == ('3', '3')


@microtest.test
def test_arg_parse_missing_values():
    options_set = False
    
    def set_option(*args):
        options_set = True
    
    options = {
        'option2': (1, lambda args: set_option(*args)),
    }
    cli_arguments = ['option2']

    with io.StringIO() as stream:
        with contextlib.redirect_stderr(stream):
            parse_args(cli_arguments, options)
            output = stream.getvalue()
            assert not options_set
            assert 'expected additional arguments' in output.lower()


@microtest.test
def test_arg_parse_missing_values():
    options_set = False
    
    def set_option(*args):
        options_set = True
    
    options = {
        'option1': (0, lambda args: set_option(*args)),
    }
    cli_arguments = ['unknown', 'option1']

    with io.StringIO() as stream:
        with contextlib.redirect_stderr(stream):
            parse_args(cli_arguments, options)
            output = stream.getvalue()
            assert not options_set
            assert 'unknown option' in output.lower()


if __name__ == '__main__':
    microtest.run()