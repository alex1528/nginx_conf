#-*- coding: utf-8 -*-

""" 生成一个全局递增 id.

"""

import redis

from libs import redisoj
from web.const import REDIS_DB_NGINX


_redis_oj = redisoj.PooledConnection(REDIS_DB_NGINX)
client = _redis_oj.get() 


def get():
    pipe = client.pipeline()

    while 1:
        try:
            pipe.watch('global_id')
            current_id = pipe.get('global_id')
            if current_id is None:
                next_id = 1
            else:
                next_id = int(current_id) + 1
            pipe.multi()
            pipe.set('global_id', next_id)
            pipe.execute()
            break
        except redis.exceptions.WatchError:
            continue
        finally:
            pipe.reset()

    return next_id


if __name__ == '__main__':
    get()
