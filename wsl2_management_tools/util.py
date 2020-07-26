# ==================================================================
#       文 件 名: util.py
#       概    要: 工具模块
#       作    者: IT小强 
#       创建时间: 2020/7/26 11:19
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from os import environ, mkdir
from os.path import expanduser, expandvars, join
from pathlib import Path


def get_user_home_path() -> str:
    """
    获取用户主目录
    :return:
    """

    user_home_path: str = ''

    try:
        user_home_path = environ['HOME']
    except KeyError:
        user_home_path = expanduser('~')
        if not user_home_path:
            user_home_path = expandvars('$HOME')
    finally:
        return user_home_path


def create_settings_path(path_name: str = '.wsl2_management_tools') -> str:
    """
    创建并返回配置目录
    :param path_name:
    :return:
    """

    user_home_path = get_user_home_path()
    settings_path = join(user_home_path, path_name)
    if not Path(settings_path).is_dir():
        mkdir(settings_path)

    return settings_path
