import redis

from .config import _cfg, _cfgi

prefix = _cfg('redis', 'prefix')
redis = redis.StrictRedis(_cfg('redis', 'host'), _cfgi('redis', 'port'))

key = lambda k: '%s.%s' % (prefix, k)