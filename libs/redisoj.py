#-*- coding: utf-8 -*-

import redis

#from web.const import REDIS_HOST, REDIS_PORT, REDIS_PASSWD
from web.const import REDIS_HOST, REDIS_PORT


class PooledConnection(object):
    def __init__(self, redis_db):
        self.pool = redis.connection.BlockingConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=redis_db,
            #password=REDIS_PASSWD,
            max_connections=10,
            timeout=60
        )

    def get(self):
        """ 返回一个连接.

        """
        return redis.client.Redis(connection_pool=self.pool)
