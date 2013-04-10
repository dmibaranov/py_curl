import pytest  # NOQA


def test_module():
    from types import ModuleType
    import py_curl
    assert isinstance(py_curl, ModuleType) is True


def test_import():
    from py_curl import curl  # NOQA


def test_simple_run_local():
    from py_curl import curl
    curl('hello.py')


def test_simple_run_remote():
    from py_curl import curl
    curl('https://raw.github.com/d9frog9n/py_curl/master/hello.py')
