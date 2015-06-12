#-*- coding: utf-8 -*-

""" 获取, 修改和删除 Nginx upstream 信息.

"""

import numbers

from libs import log

from web import const
from nginx.libs import mysqloj


logger = log.get_logger("Nginx UPSTREAM ")


def get():
    """ 获取 upstream 信息.

    """
    _mysql_oj = mysqloj.PooledConnection()
    sql = "select name, loki_id, port, ip_hash, online "\
          "from %s;" % const.MYSQL_TABLE
    ret = _mysql_oj.select(sql) 

    data = list()
    for i in ret:
        _dict = {
            "name": i[0],
            "loki_id": i[1],
            "port": i[2],
            "ip_hash": i[3],
            "online": i[4]
        }
        data.append(_dict)
    return data


def add(name, loki_id, port, ip_hash, online):
    """ 增加 upstream.

    """
    if not (isinstance(loki_id, numbers.Integral) and isinstance(port, numbers.Integral)):
        raise("loki_id and port must be int.")

    if ip_hash not in [0, 1] or online not in [0, 1]:
        raise("ip_hash and online must be 0 or 1.")

    sql = """insert into %s (name, loki_id, port, ip_hash, """\
          """online) values ("%s", %s, %s, %s, %s); """ % (const.MYSQL_TABLE, 
                                                           name, loki_id, 
                                                           port, ip_hash, online)
    return _exec_change_sql(sql)


def modify(name, _dict):
    """ 根据 name 修改 upstream.

    _dict 格式是:
        {
            "loki_id": loki_id,
            "port": port,
            "ip_hash": ip_hash,
            "online": online
        }
    key 可以一个或多个.

    """
    _set_str = list()
    for key, value in _dict.items():
        _set_str.append("%s=%s" % (key, value))
    sql = "update %s set %s where %s.name='%s'" % (const.MYSQL_TABLE, 
                                                   ",".join(_set_str), 
                                                   const.MYSQL_TABLE, 
                                                   name)
    return _exec_change_sql(sql)


def delete(name):
    """ 根据 name 删除 upstream.

    """
    sql = "delete from %s where name='%s' " % (const.MYSQL_TABLE, name)
    return _exec_change_sql(sql)


def _exec_change_sql(sql):   
    """ 执行会改变数据库的 sql.

    """
    _mysql_oj = mysqloj.PooledConnection()
    status, result = _mysql_oj.change(sql)
    message = "sql:%s, status:%s, result:%s" % (sql, status, result)
    logger.info(message)
    return (status, result)
