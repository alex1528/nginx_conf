#!/usr/bin/env python
#-*- coding: utf-8 -*-


import socket
import sys
import os

import ujson as json

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.auth
import tornado.web
import tornado.escape
import tornado.netutil

from web.const import BIND_IP
from web.const import BIND_PORT
from nginx.web import service as nginx_service


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            #(r"/api/v1/nginx/?", nginx_service.WstypeHander),
            (r"/api/v1/nginx/conf/?", nginx_service.ConfHandler),
            (r"/api/v1/nginx/branches/?", nginx_service.BranchesHandler),
            (r"/api/v1/nginx/upstreams/([^/]+)/?", nginx_service.UpstreamHandler),
            (r"/api/v1/nginx/upstreams/?", nginx_service.UpstreamsHandler),
            (r"/api/v1/nginx/domains/?", nginx_service.DomainsHandler)        
        ]

        settings = {}

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    application = Application()

    sockets = tornado.netutil.bind_sockets(
        BIND_PORT, address=BIND_IP, family=socket.AF_INET)
    tornado.process.fork_processes(0)

    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
