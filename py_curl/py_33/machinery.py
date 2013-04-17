import py_curl

class PostRemoteFinder(object):
    def find_module(self, fullname, path=None):
        import pdb;pdb.set_trace()
        return None
        return PostRemoteLoader

class PostRemoteLoader(object):
    def load_module(self, fullname):
        pass
