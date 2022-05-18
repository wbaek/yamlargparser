import os
import pytest

from yamlargparser import ArgumentParser

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'arguments.yaml')
)
def test_parser(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ArgumentParser()
    options = parser.parse_args(['-c', filenames[0]])
    # args = parser.parse_args(args=['-c', filenames[0]])

    assert options.foo == 'test'
    assert options.bar == 1234

    flags, options = parser.parse_args(['-c', filenames[0]], return_dict=True)
    assert options['foo'] == 'test'
    assert options['bar'] == 1234


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'arguments.yaml')
)
def test_parser(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ArgumentParser()
    parser.add_argument('--add', type=str, default='add')
    options = parser.parse_args(['-c', filenames[0]])
    # args = parser.parse_args(args=['-c', filenames[0]])

    assert options.foo == 'test'
    assert options.bar == 1234
    assert options.add == 'add'

    flags, options = parser.parse_args(['-c', filenames[0]], return_dict=True)
    assert options['foo'] == 'test'
    assert options['bar'] == 1234
    assert flags.add == 'add'


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'arguments.yaml')
)
def test_parser_update(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ArgumentParser()
    options = parser.parse_args(args=['-c', filenames[0]] + ['--foo', 'value'])
    assert options.foo == 'value'
    assert options.bar == 1234

    flags, options = parser.parse_args(args=['-c', filenames[0]] + ['--foo', 'value'], return_dict=True)
    assert options['foo'] == 'value'
    assert options['bar'] == 1234


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'arguments.yaml')
)
def test_arguments_boolean(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ArgumentParser()
    args = parser.parse_args(args=['-c', filenames[0], '--var', 'true'])
    assert args.var == True

    flags, args = parser.parse_args(args=['-c', filenames[0], '--var', 'true'], return_dict=True)
    assert args['var'] == True

    parser = ArgumentParser()
    args = parser.parse_args(args=['-c', filenames[0], '--var', 'false'])

    flags, args = parser.parse_args(args=['-c', filenames[0], '--var', 'no'], return_dict=True)
    assert args['var'] == False


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'arguments.yaml')
)
def test_arguments_invalid(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ArgumentParser()
    with pytest.raises(SystemExit) as e:
        _ = parser.parse_args(args=['-c', filenames[0], '--baz', 'test'])
    # pytest: error: unrecognized arguments: --baz test

    parser = ArgumentParser()
    with pytest.raises(SystemExit) as e:
        _ = parser.parse_args(args=['-c', filenames[0], '--bar', 'test'])
    # pytest: error: argument --bar: invalid int value: 'test'

    parser = ArgumentParser()
    with pytest.raises(Exception) as e:
        parser.add_argument('--foo', type=int, default=1)
        _ = parser.parse_args(args=['-c', filenames[0], '--bar', 'test'])
    assert str(e.value) in ['argument --foo: conflicting option string: --foo',
                            'argument --foo: conflicting option string(s): --foo']
