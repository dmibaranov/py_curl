import sys

from py_curl.loader import Loader


def curl(*args, **kwargs):
    loader = Loader(*args, **kwargs)
    modules = loader.modules
    p_locals = sys._getframe(1).f_locals
    for m in modules:
        p_locals[m] = loader.modules[m]
