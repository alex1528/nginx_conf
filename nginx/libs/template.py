#-*- coding: utf-8 -*-

"""  生成 upstream nodes 的配置文件.

"""


from jinja2 import Environment, FileSystemLoader


def gen_upstream(template_dir, template_file, template_dest, data):
    """ 生成 upstream nodes 配置文件.

    data 是一个 list, list 里面是一个 dict, dict
    里面有 node_name, servers, port, servers 又是
    一个 list.

    """
    j2_env = Environment(loader=FileSystemLoader(template_dir),
                         trim_blocks=True)
    ret = j2_env.get_template(template_file).render(data=data)
    with file(template_dest, 'w') as f:
        f.writelines(ret)


def gen_server(template_dir, template_file, template_dest,
               server_names, log_name, log_format, upstream_node):
    """ 生成 server 配置文件.

    传入变量:
        server_names
        log_name
        log_format
        upstream_node

    """
    j2_env = Environment(loader=FileSystemLoader(template_dir),
                         trim_blocks=True)
    ret = j2_env.get_template(template_file).render(server_names = server_names,
                                                    log_name = log_name,
                                                    log_format = log_format,
                                                    upstream_node = upstream_node)
    with file(template_dest, 'w') as f:
        f.writelines(ret)
