import os
import shutil
import sys
import tempfile


if sys.version_info.major == 3 and sys.version_info.minor >= 3:
    impl = 'py_33'
else:
    impl = 'py_old'

__path__.append(os.path.join(os.path.dirname(__file__), impl))


from py_curl.downloader import Downloader
from py_curl.machinery import PostRemoteFinder
from py_curl.logger import logger


sys.path_hooks += [PostRemoteFinder]


LOOPS = set(['sync'])
try:
    import gevent  # NOQA
    LOOPS.append('gevent')
except ImportError:
    logger.debug('gevent loop is not availible')

try:
    import tulip  # NOQA
    LOOPS.append('tulip')
except ImportError:
    logger.debug('tulip loop is not availible')


class TempDirsGC(object):
    def __init__(self):
        self._temp_dirs = []

    def new_temp_dir(self):
        temp_dir = tempfile.mkdtemp(prefix='py_curl')
        self._temp_dirs.append(temp_dir)
        return temp_dir

    def __del__(self):
        for d in self._temp_dirs:
            shutil.rmtree(d, ignore_errors=True)


_TDGC = TempDirsGC()


def curl(*args, **kwargs):
    p_locals = sys._getframe(1).f_locals

    kwargs['temp_dir'] = _TDGC.new_temp_dir()

    downloader = Downloader(*args, **kwargs)
    for module_name, module_details in downloader.modules.items():
        sys.path += [os.path.dirname(module_details['path'])]
        module = __import__(module_name)
        p_locals[module_details.get('alias') or module.__name__] = module
