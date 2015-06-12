#-*- coding: utf-8 -*-

import requests


def get_path_from_hostname(hostname):
    url = "http://loki.internal.nosa.me"\
          "/ptree/api/server_search?hostname=%s" % hostname

    ret = requests.get(url)
    dirs = ret.json()["data"]["dirs"]
    return [i["dir"] for i in dirs]


def get_hostnames_from_id(node_id):
    url = "http://loki.internal.nosa.me"\
          "/server/api/servers?type=recursive&node_id=%s" % node_id

    ret = requests.get(url)
    data = ret.json()["data"]
    return [i["hostname"] for i in data]
