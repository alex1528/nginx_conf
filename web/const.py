#-*- coding: utf-8 -*-


# 绑定 IP 和 端口.
BIND_IP = "0.0.0.0"
BIND_PORT = "8084"

# 日志路径.
LOG_DIR = "./logs/"
LOG_FILE = "nginx_conf.log"

# REDIS 信息.
REDIS_HOST = ""
REDIS_PORT = 6379
REDIS_DB_NGINX = "0"

# Nginx 信息.
NGINX_CONF_DIR = "/home/work/nginx_cfg/"   # Nginx git 项目配置文件.
NGINX_TMP_STORAGE_DIR = "nginx_conf/"   # 临时存储 Nginx 配置主目录.
NGINX_UPSTREAM_TEMPLATE_DIR = "nginx/template/"
NGINX_UPSTREAM_TEMPLATE_FILE = "upstream.conf"

# Nginx ssl 证书文件, ssl 证书放在 git 中不安全, 这里从 NGINX_SSL_ORIGIN_DIR
# 拷贝到 NGINX_CONF_DIR 目录下的 NGINX_SSL_DEST_DIR 目录里.
NGINX_SSL_ORIGIN_DIR = ""
NGINX_SSL_DEST_DIR = ""

# Nginx upstream nodes 信息放在数据库里.
MYSQL_USER = ""
MYSQL_PASSWD = "" 
MYSQL_HOST = ""
MYSQL_PORT = 3306 
MYSQL_DATABASE = ""
MYSQL_TABLE = ""
