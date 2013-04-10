import os
import shutil
import sys
import tempfile

from py_curl.cross_python import string_type, urlopen, urlparse
from py_curl.logger import logger


__all__ = ['Loader']

LOOPS = set(['sync'])
try:
    __import__('gevent')
    LOOPS.append('gevent')
except ImportError:
    logger.debug('gevent loop is not availible')

try:
    __import__('tulip')
    LOOPS.append('tulip')
except ImportError:
    logger.debug('tulip loop is not availible')


class Loader(object):

    def __init__(self, deps={}, callback=None, loop_type='sync'):
        self.dep_names = {}
        if isinstance(deps, string_type):
            self.dep_names[0] = deps
        elif isinstance(deps, dict):
            self.dep_names = deps
        elif '__iter__' in dir(deps):
            self.dep_names = dict(zip(enumerate(set(deps))))

        self.callback = callback
        self.loop_type = loop_type
        self.modules = {}
        self._temp_dirs = []

        self.load()

    def load(self):
        logger.debug('Starting loading')

        if self.loop_type not in LOOPS or self.loop_type == 'sync':
            self._load_deps_sync()
        else:
            loader = getattr(self, '_load_deps_' + self.loop_type, None)
            if not loader:
                raise NotImplementedError('%(cls)s._load_deps_%(loop)s '
                                          'is not implemented' %
                                          dict(cls=self.__class__.__name__,
                                               loop=self.loop_type))
            else:
                loader()

        logger.debug('Loading finished')
        if self.callback and getattr(self.callback, '__call__'):
            logger.debug('Calling callback')
            self._callback()

    def _load_deps_sync(self):
        for name, dep_path in self.dep_names.copy().items():
            kwargs = dict(dep=dep_path)
            if isinstance(name, string_type):
                kwargs.update(module_name=name)
            self._load_dep_sync(**kwargs)

    def _load_dep_sync(self, dep, module_name=None):
        logger.debug('Loading %s dep' % dep)
        mod = None

        c = urlparse.urlparse(dep)
        if not c.scheme or c.scheme == 'file':
            mod = self._import(c.path)
        elif c.scheme in ('http', 'https'):
            response = urlopen(dep)

            tmp_dir = tempfile.mkdtemp()

            with open(os.path.join(tmp_dir, '__init__.py'), 'wt') as init_file:
                init_file.write('#make a package')

            temp_full_path = os.path.join(tmp_dir, os.path.basename(dep))
            with open(temp_full_path, 'wt') as module_file:
                module_file.write(str(response.read()))

            mod = self._import(temp_full_path)
            self._temp_dirs.append(tmp_dir)
        if mod:
            self.modules[module_name or mod.__name__] = mod

    def _import(self, path):
        sys.path.append(os.path.dirname(path))
        module_name = extract_module_name(path)
        return __import__(module_name)

    def then(self, callback=None):
        if callback and getattr(callback, '__call__'):
            logger.debug('Calling then-callback')
            callback()

    def __del__(self):
        for d in self._temp_dirs:
            shutil.rmtree(d, ignore_errors=True)


def extract_module_name(path):
    name = os.path.basename(path)
    if name.endswith('.py'):
        name = name[:-3]
    return name
