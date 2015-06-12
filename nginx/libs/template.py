#-*- coding: utf-8 -*-

"""  生成 upstream nodes 的配置文件.

"""

from jinja2 import Environment, FileSystemLoader


def gen(template_dir, template_file, template_dest, data):
    """ 生成 upstream nodes 配置文件.

    data 是一个 list, list 里面是一个 dict, dict 
    里面有 node_name, servers, port, servers 又是
    一个 list.

    """
    j2_env = Environment(loader=FileSystemLoader(template_dir),
                         trim_blocks=True)
    ret = j2_env.get_template(template_file).render(
        data=data,
    )
    with file(template_dest, 'w') as f:
        f.writelines(ret)
