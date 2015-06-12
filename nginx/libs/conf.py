#-*- coding: utf-8 -*-

""" 返回 Nginx 配置文件的下载地址.

"""

import os
import re
import functools

from libs import log, utils, loki, redisoj, storage
from web.const import (NGINX_CONF_DIR, 
                       NGINX_TMP_STORAGE_DIR, 
                       NGINX_UPSTREAM_TEMPLATE_DIR, 
                       NGINX_UPSTREAM_TEMPLATE_FILE, 
                       NGINX_SSL_ORIGIN_DIR, 
                       NGINX_SSL_DEST_DIR, 
                       REDIS_DB_NGINX)
from nginx.libs import global_id, template, upstream


_redis_oj = redisoj.PooledConnection(REDIS_DB_NGINX)
client = _redis_oj.get() 

logger = log.get_logger("Nginx CONF ")


def _shell(cmd, _logger=logger):
    """ 执行命令, 记录日志.

    """
    rc , so, se = utils.shell(cmd)
    if rc == 0:
        message = "cmd:%s" % cmd
        _logger.info(message)
    else:
        message = "cmd:%s, error:%s" % (
            cmd, se)
        raise Exception(message)


def _redis_lock(func):
    """ redis 锁.

    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        while 1:
            if client.exists("lock"):
                import time
                time.sleep(0.1)
            else:
                client.set("lock", None, 2)   # 2s 超时.
                return func(*args, **kw)
                client.delete("lock")
                break
    return wrapper


@_redis_lock
def _conf(branch, conf_base_dir, conf_tmp_dir):
    """ 拉取配置并拷贝到响应目录.
    
    由于 git 并发操作会报错, 所以用了 redis 锁.

    """
    # 拷贝最新 Nginx 配置.
    cmd = """cd %s &&\
        git fetch origin -p &&\
        git checkout %s &&\
        git pull &&\
        cp -a %s %s """ % ( conf_base_dir, 
                            branch, 
                            conf_base_dir, 
                            conf_tmp_dir)
    _shell(cmd)


def get(nginx, branch):
    """ 根据 Nginx 机器名打包配置文件, 并上传到远端和获取下载地址.

    """
    # 拿到 Nginx 机器的 产品线,类型,机房.
    loki_path = loki.get_path_from_hostname(nginx)
    if loki_path == []:
        raise Exception("%s has no loki path." % nginx)
    elif len(loki_path) > 1:
        raise Exception("%s has %s loki path - %s." % (
                            nginx, 
                            len(loki_path), 
                            loki_path))

    tmp = loki_path[0].split("/")
    product = tmp[2]   # 产品线
    _type = tmp[-2]   # 类型, 表示内网还是内网.
    idc = tmp[-1]    # 机房.
    del tmp
    logger.info("%s %s %s" % (product, _type, idc))

    # 创建临时 Nginx 配置文件目录.
    if not os.path.exists(NGINX_TMP_STORAGE_DIR):
        os.mkdir(NGINX_TMP_STORAGE_DIR)
    _global_id = global_id.get()
    conf_tmp_dir = "%s/%s/%s" % (os.getcwd(), 
                                 NGINX_TMP_STORAGE_DIR, 
                                 _global_id)

    # 拷贝最新 Nginx 配置.
    _conf(branch, NGINX_CONF_DIR, conf_tmp_dir)

    # 拿到 upstream data.
    upstream_data = list()
    for i in upstream.get():
            if i["online"] == 1:
                servers = loki.get_hostnames_from_id(i["loki_id"])
                if servers == []:
                    raise("%s has no servers." % i["loki_id"])
                _dict = {
                    "name": i["name"],
                    "servers": servers,
                    "port": i["port"],
                    "ip_hash": i["ip_hash"]
                }
                upstream_data.append(_dict)

    # 生成 upstream.conf 文件.
    upstream_path = "%s/upstream.conf" % conf_tmp_dir
    template.gen(NGINX_UPSTREAM_TEMPLATE_DIR, 
                 NGINX_UPSTREAM_TEMPLATE_FILE, 
                 upstream_path, 
                 upstream_data)

    # 做软链.
    cmd = "sh nginx/libs/link.sh %s %s %s %s %s %s" % (conf_tmp_dir, product, 
                                                       _type, idc, 
                                                       NGINX_SSL_ORIGIN_DIR, 
                                                       NGINX_SSL_DEST_DIR)
    _shell(cmd)

    # 打包.
    package_name = "%s.tgz" % _global_id
    cmd = "cd %s &&tar czf ../%s *" % (conf_tmp_dir, 
                                       package_name)
    _shell(cmd)

    # 把 Nginx 包上传到存储服务, 并返回下载连接.
    package_path = "%s/%s" % (NGINX_TMP_STORAGE_DIR, package_name)
    logger.info("package_path:%s" % package_path)
    return storage.post(package_path)
