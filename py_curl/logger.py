import sys
import logging

logger = logging.getLogger('pycurl')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
