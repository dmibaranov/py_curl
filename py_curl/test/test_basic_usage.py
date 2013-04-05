import pytest

def test_module():
    from types import ModuleType
    import py_curl
    assert isinstance(py_curl, ModuleType) == True

def test_import():
    from py_curl import curl


def t1est_simple_run():
    from py_curl import curl
    curl('hello.py')


def t1est_invalid_run():
    from py_curl import curl
    with pytest.raises(TypeError):
        curl()


def t1est_run():
    from py_curl import curl
    from py_curl.loader import Curl

    assert curl == curl_loader
