# 说明

Nginx 配置管理, 基于 git, 并分产品线, 内网外网和机房三个维度.


    1. 由于 Nginx 配置分为 产品线、内网或外网和机房, 不同纬度的 Nginx 的配置不一样;
    
    2. 支持分支发布, 根据 Nginx 机器名和分支名获取配置文件链接;

    3. 提供获取和增删改 Nginx upstream API;

    4. Nginx upstream 信息放在 mysql, 根据模板生成upstream.conf, 机器列表实时从服务管理系统获取;

    5. 支持 ip_hash 字段, online 字段表示 是否在线, 不为1 不生成配置;

    6. 支持增加域名, 自动生成配置文件并 push 到 origin.




# Nginx upstream 数据库
```
create database online_nginx_conf;
create table nginx_upstream_template (
    id int unsigned not null auto_increment,
    name varchar(100) not null,
    loki_id int unsigned not null,
    port int unsigned not null default 80,
    ip_hash int unsigned not null default 0,
    online int unsigned not null default 1,
    primary key (id),
    unique KEY `unq_name` (`name`);
);
```



# 依赖

```
pip install futures

pip install ujson

pip install tornado

pip install DBUtils

pip install jinja2

yum -y install python-redis python-ldap MySQL-python```
```
