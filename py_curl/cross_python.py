import sys


if sys.version_info >= (3,):
    from urllib import parse as urlparse  # NOQA
    from urllib.request import urlopen

    string_type = str
else:
    import urlparse  # NOQA
    from urllib import urlopen  # NOQA
    string_type = basestring
