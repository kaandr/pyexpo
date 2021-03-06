from pyexpo import explore_paths, PySpace, Package
from pyexpo.utils import abs_dir
import os

DATA_DIR = abs_dir(__file__) / 'data'

PATH1      = abs_dir(DATA_DIR) / 'path1'
PATH2      = abs_dir(DATA_DIR) / 'path2'
PATH_BASIC = abs_dir(DATA_DIR) / 'basic'

PATHS = (PATH1, PATH2, PATH_BASIC)


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test__simple():
    names = {i.name for i in explore_paths(PATHS)}
    assert 'pkg_bar' in names


def test__toplevel_package():
    space = PySpace(only_paths=PATHS)
    p = space['foo']
    # variants:
    #p = space.get('foo')
    #p = space['foo']
    #p = space.foo
    assert isinstance(p, Package)


def test__package_children():
    space = PySpace(only_paths=PATHS)
    foo = space['foo']
    submodule_names = {m.name for m in foo.children}
    expected = {'foo.subfoo', 'foo.bar', 'foo.__main__', 'foo.print_dir'}
    assert expected == submodule_names


def test__is_package_callable():
    space = PySpace(only_paths=PATHS)
    foo = space['foo']
    assert foo.callable


def test__is_package_not_callable():
    space = PySpace(only_paths=PATHS)
    foo = space['pkg_bar']
    assert not foo.callable


def test__dictlike_package_access():
    space = PySpace(only_paths=[PATH1])
    assert space['foo']['subfoo'].name == 'foo.subfoo'


def test__subpackage_func():
    space = PySpace(only_paths=[PATH1])
    assert space['foo']['bar']['func'].name == 'foo.bar.func'


def test__function_arguments():
    #foo.bar.func(a,b='2')
    space = PySpace(only_paths=[PATH1])
    assert space['funcs']['sum'].arguments.args == ['arg1']
    assert space['funcs']['sum'].arguments.kwargs == (('kwarg1', 1),)


def test__function_call():
    space = PySpace(only_paths=[PATH1])
    assert space['funcs']['sum'].call(3, 4) == 7


def test__package_call(capsys):
    space = PySpace(only_paths=[PATH1])
    space['foo'].call()
    out, err = capsys.readouterr()
    assert out == 'Loading __main__\nRunning __main__\n' 


def test__module_call(capsys):
    space = PySpace(only_paths=[PATH1])
    space['foo']['bar'].call()
    out, err = capsys.readouterr()
    assert out == 'Loading bar\nRunning bar\n' 


#def test__process_load_error():
#    def on_error(exc, object_name, 
#    space = PySpace(only_paths=[PATH2], on_error=)

#: set autocmd BufWritePost * !py.test
