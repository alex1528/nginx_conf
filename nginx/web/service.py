#-*- coding: utf-8 -*-


import socket
import sys
import os

import ujson as json
from concurrent.futures import ThreadPoolExecutor

import tornado.web
from tornado import gen

from libs import utils
from lvs.libs import info
from nginx.libs import wstype, conf, upstream
from web.const import NGINX_CONF_DIR


def _self_write(status, name, func, fail_msg=None, succ_msg=None):
    """ 代码重用.

    """
    if fail_msg is None:
        fail = {
            "status": "failed",
            "message": "%s %sed failed" % (name, func)
        }
    else:
        fail = {
            "status": "failed",
            "message": fail_msg
        }

    if succ_msg is None:
        succ = {
            "status": "success",
            "message": "%s has been %sed successfully" % (name, func)
        }
    else:
        succ = {
            "status": "success",
            "message": succ_msg
        }

    if status:
        return json.dumps(succ)
    else:
        return json.dumps(fail)


#class WstypeHander(tornado.web.RequestHandler):
#
#    def get(self):
#        """ 拿到每一个 wstype 的 Nginx 列表.
#
#        """
#        cluster_nginxs = list()
#        _list = list()
#    
#        for cluster_lvs in info.cluster():
#            for vip2ws in cluster_lvs["vip2ws"]:
#                _dict = {}
#                _wstype = "%s:%s" % (cluster_lvs["name"], vip2ws["wstype"])
#                if _wstype not in _list:
#                    _dict["wstype"] = _wstype
#                    _dict["wss"] = vip2ws["wss"]
#                    cluster_nginxs.append(_dict)
#                    _list.append(_wstype)
#                else:
#                    for cluster_nginx in cluster_nginxs:
#                        if cluster_nginx["wstype"] == _wstype:
#                            cluster_nginx["wss"].extend(vip2ws["wss"])
#        
#        # wss 列能有重复, 需清理.
#        for cluster_nginx in cluster_nginxs:
#            cluster_nginx["wss"] = {}.fromkeys(cluster_nginx["wss"]).keys()
#
#        self.write(json.dumps(cluster_nginxs))


class ConfHandler(tornado.web.RequestHandler):
    global executor
    executor = ThreadPoolExecutor(max_workers=3)

    @tornado.gen.coroutine
    def get(self):
        """ 根据 Nginx 机器生成 Nginx 配置文件包和并返回下载链接.

        """
        nginx = self.get_argument('nginx')
        branch = self.get_argument('branch')

        _ret = yield executor.submit(conf.get, nginx, branch)
        ret = {
            "status": "success",
            "message": _ret
        }
        self.write(json.dumps(ret))


class BranchesHandler(tornado.web.RequestHandler):

    def get(self):
        """ 返回 Nginx 的分支.

        """
        cmd = "cd %s &&git fetch origin &&git branch -r" % NGINX_CONF_DIR
        rc, so, se = utils.shell(cmd)    
        branches = [
            i.strip().replace("origin/", "") 
            for i in so.strip().splitlines() 
            if "origin/HEAD" not in i
        ]
        self.write(json.dumps(branches))


class UpstreamsHandler(tornado.web.RequestHandler):

    def get(self):
        """ 返回 upstream 列表.

        """
        self.write(json.dumps(upstream.get()))

    def post(self):
        """ 增加 upstream. 

        """
        name = json.loads(self.get_argument('name'))
        loki_id = json.loads(self.get_argument('loki_id'))
        port = json.loads(self.get_argument('port'))
        ip_hash = json.loads(self.get_argument('ip_hash'))
        online = json.loads(self.get_argument('online'))
        status, result = upstream.add(name, loki_id, port, ip_hash, online)
        self.write(_self_write(status, name, "add", result))


class UpstreamHandler(tornado.web.RequestHandler):

    def patch(self, name):
        """ 增加 upstream. 

        """
        data = json.loads(self.get_argument('data'))
        status, result = upstream.modify(name, data)
        self.write(_self_write(status, name, "modify", result))

    def delete(self, name):
        """ 删除  upstream.

        """
        status, result = upstream.delete(name)
        self.write(_self_write(status, name, "delet", result))
