# -*- coding: utf-8 -*-

import MySQLdb
from DBUtils import PooledDB
 
from web import const


class PooledConnection(object):
    def __init__(self):
        self.pool = PooledDB.PooledDB(MySQLdb, 
            user=const.MYSQL_USER, 
            passwd=const.MYSQL_PASSWD, 
            host=const.MYSQL_HOST, 
            port=const.MYSQL_PORT, 
            db=const.MYSQL_DATABASE, 
            mincached=3, 
            maxcached=10, 
            maxshared=3, 
            maxconnections=100
        )

    def get(self):
        """ 返回一个数据库连接.

        """
        return self.pool.connection()

    def select(self, sql):
        """ 查询数据库.

        """
        conn = self.get()
        cur = conn.cursor()
        cur.execute(sql)
        # res = cur.fetchone()
        res = cur.fetchall()
        cur.close() 
        conn.close()
        return res

    def change(self, sql):
        """ 修改数据库.

        """
        conn = self.get()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            return (True, None)
        except Exception, e:
            conn.rollback()
        finally:
            cur.close()
            conn.close()

        return (False, "%s" % e)

    def sqls(self, _sqls):
        """ 多条 sql 事务执行.

        """
        conn = self.get()
        cur = conn.cursor()
        try:
            # cur.execute("set autocommit=0 ")
            for sql in _sqls:
                cur.execute(sql)
            conn.commit()
            res = cur.fetchall()
            return (True, res)
        except Exception, e:
            conn.rollback()
        finally:
            cur.close()
            conn.close()

        return (False, "%s" % e)
