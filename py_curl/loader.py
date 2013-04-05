import os
import sys
import urlparse

import requests

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

    def __init__(self, deps, callback=None, loop_type='sync'):
        self.dep_names = []
        if isinstance(deps, basestring):
            self.dep_names = tuple([deps])
        #elif isinstance(deps, dict):
        #    self.dep_names = deps
        elif '__iter__' in dir(deps):
        #    self.dep_names = dict(zip(enumerate(deps)))
            self.dep_names = tuple(deps)
        else:
            pass

        self.callback = callback
        self.loop_type = loop_type
        self.modules = {}

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

    def _load_deps_sync(self):
        for d in self.dep_names:
            self._load_dep_sync(d)
        self._after_load()

    def _load_dep_sync(self, dep):
        logger.debug('Loading %s dep' % dep)
        c = urlparse.urlparse(dep)
        if c.scheme == 'file':
            mod = self._import(c.path)
        elif c.scheme in ('http', 'https'):
            r = requests.get(dep)
        if mod:
            self.modules[mod.__name__] = mod


    def _import(self, path):
        sys.path.append(os.path.dirname(path))
        return __import__(os.path.basename(path)[:-2])

    def _after_load(self):
        logger.debug('Loading finished')
        if self.callback and getattr(self.callback, '__call__'):
            logger.debug('Calling callback')
            self._callback()

    def then(self, callback=None):
        if callback and getattr(callback, '__call__'):
            logger.debug('Calling then-callback')
            callback()
