#-*- coding: utf-8 -*-

""" 返回 Nginx 配置文件的下载地址.

"""


import os

from libs import log, utils
from web.const import (NGINX_CONF_DIR, 
                       NGINX_TEMPLATE_DIR,
                       NGINX_SERVER_TEMPLATE_FILE)
from nginx.libs import template, upstream


logger = log.get_logger("Nginx DOMAINS ")


def _shell(cmd, _logger=logger):
    """ 执行命令, 记录日志.

    """
    rc , so, se = utils.shell(cmd)
    if rc == 0:
        message = "cmd:%s" % cmd
        _logger.info(message)
    else:
        message = "cmd:%s, error:%s" % (cmd, se)
        raise Exception(message)


def add(product, _type, idc, name, server_names, log_name, log_format, upstream_node):
    """ 增加域名的配置.

    """
    upstreams = upstream.get()
    upstream_nodes = [ i["name"] for i in upstreams ]
    if upstream_node not in upstream_nodes:
        raise Exception("%s not exist" % upstream_node)
    else:
        for i in upstreams:
            if i["name"] == upstream_node:
                if i["online"] != 1:
                    raise Exception("%s is offline" % i["name"])
                else:
                    break

    domain_conf_dir = "%s/sites-available/%s/%s/%s/" % (NGINX_CONF_DIR,
                                                        product,
                                                        _type,
                                                        idc)
    domain_conf_path = "%s/%s" % (domain_conf_dir, name)
    
    if not os.path.exists(domain_conf_dir):
        os.makedirs(domain_conf_dir)

    if os.path.exists(domain_conf_path):
        raise("%s exists" % domain_conf_path)

    template.gen_server(NGINX_TEMPLATE_DIR, NGINX_SERVER_TEMPLATE_FILE, 
                        domain_conf_path, server_names, log_name, 
                        log_format, upstream_node)

    cmds = """cd %s &&
        git checkout master &&
        git pull &&
        git add sites-available/%s/%s/%s/%s &&
        git commit -m 'add %s' &&
        git push origin master """ % (NGINX_CONF_DIR, product, 
                                      _type, idc, name, name)

    _shell(cmds)
    return True
