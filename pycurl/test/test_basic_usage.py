import pytest

def test_module():
    from types import ModuleType
    import pycurl
    assert isinstance(pycurl, ModuleType) == True

def test_import():
    from pycurl import curl


def t1est_simple_run():
    from pycurl import curl
    curl('hello.py')


def t1est_invalid_run():
    from pycurl import curl
    with pytest.raises(TypeError):
        curl()


def t1est_run():
    from pycurl import curl
    from pycurl.loader import Curl

    assert curl == curl_loader
