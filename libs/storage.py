#-*- coding: utf-8 -*-

""" 把一个文件存储到下载服务, 并返回 下载链接.

"""

import os

from libs import utils


def post(file_path):
    """ 上传文件到远程并拿到下载链接.

    使用封装过的 wcdn 命令.

    """
    cmd = " wcdn cp -f %s /cdn.internal.nosa.me/nginx_conf_deploy "\
            "--no-verbose --md5" % file_path
    rc, so, se = utils.shell(cmd)
    if rc != 0:
        raise Exception(se)

    return "http://cdn.internal.nosa.me/nginx_conf_deploy/%s"\
                % os.path.basename(file_path)
