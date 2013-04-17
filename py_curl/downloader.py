import os

#from py_curl import LOOPS
from py_curl.cross_python import string_type, urlopen, urlparse
from py_curl.logger import logger


LOOPS = []


class Downloader(object):

    def __init__(self, deps={}, loop_type='sync', temp_dir=None):
        self.dep_names = {}
        if isinstance(deps, string_type):
            self.dep_names[0] = deps
        elif isinstance(deps, dict):
            self.dep_names = deps
        #elif '__iter__' in dir(deps):
        #    self.dep_names = dict(zip(enumerate(set(deps))))

        self.loop_type = loop_type
        self.temp_dir = temp_dir

        self.modules = {}

        self.load()

    def load(self):
        logger.debug('Starting downloading')

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

        logger.debug('Downloading finished')

    def _load_deps_sync(self):
        for psedo_name, dep_path in self.dep_names.copy().items():
            kwargs = dict(dep=dep_path)
            if isinstance(psedo_name, string_type):
                kwargs.update(module_alias=psedo_name)
            self._load_dep_sync(**kwargs)

    def _load_dep_sync(self, dep, module_alias=None):
        logger.debug('Downloading %s dep' % dep)
        basename = os.path.basename(dep)

        c = urlparse.urlparse(dep)

        if not c.scheme or c.scheme == 'file':
            module_path = c.path
        elif c.scheme in ('http', 'https'):
            response = urlopen(dep)

            temp_full_path = os.path.join(self.temp_dir, basename)
            with open(temp_full_path, 'wt') as module_file:
                module_file.write(str(response.read()))
            module_path = temp_full_path

        module_name = extract_module_name(basename)
        if module_path:
            self.modules[module_name] = dict(path=module_path)
            if module_alias:
                self.modules[module_name].update(alias=module_alias)


def extract_module_name(filename):
    module_name = filename
    if filename.endswith('.py'):
        module_name = filename[:-3]
    return module_name
