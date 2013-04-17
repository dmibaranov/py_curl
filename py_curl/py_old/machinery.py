class PostRemoteFinder:
    def __init__(self, *args, **kwargs):
        print args, kwargs

    def find_module(self, fullname, path=None):
        print fullname, path
        return None
        return PostRemoteLoader()


class PostRemoteLoader:
    def load_module(self, fullname):
        print fullname
        return None
