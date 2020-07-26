# ==================================================================
#       文 件 名: settings_manage.py
#       概    要: 配置操作类，获取、保存配置
#       作    者: IT小强 
#       创建时间: 2019/12/24 18:14
#       修改时间: 
#       copyright (c) 2016 - 2019 mail@xqitw.cn
# ==================================================================

import os
from os.path import join, isfile
from json import loads, dumps

from wsl2_management_tools.util import create_settings_path


class SettingsManage:
    """
    配置操作类，获取、保存配置
    """

    # 默认配置数据
    __settings = {
        'SERVER_PORT': '9205',
        'START_BAT': ''
    }

    def __init__(self, base_dir: str):
        """
        初始化
        """

        self.settings_dir = create_settings_path(path_name=os.path.join(base_dir, '.wsl2_management_tools'))
        self.settings_file = join(self.settings_dir, 'settings.json')

        self.cmd_bat_tpl_path = os.path.join(base_dir, 'manage.bat.tpl')
        self.cmd_bat_path = os.path.join(self.settings_dir, 'manage.bat')

        self.__settings_init()

        if not os.path.exists(self.cmd_bat_path):
            self.change_start_bat(cmd='', port=self.__settings.get('SERVER_PORT'))

    def set(self, name, value):
        """
        设置配置
        @param name: 配置名称
        @param value: 配置值
        """
        self.__settings[name] = value
        self.save_file_content(self.settings_file, dumps(self.__settings))

    def get(self, name=None, default_value=None):
        """
        获取配置
        @param name: 配置名称 None 会返回全部配置
        @param default_value: 不存在时返回的默认值
        @return: 返回配置值
        """
        if not name:
            return self.__settings
        return self.__settings.get(name, default_value)

    def __settings_init(self):
        """
        读取json文件的内容并转为字典
        """

        # 如果文件不存在则创建文件
        if not isfile(self.settings_file):
            self.save_file_content(self.settings_file, dumps(self.__settings))

        # 读取文件内容
        with open(self.settings_file, 'r') as f:
            content = f.read()

        # 转为json
        self.__settings.update(loads(content))

    @staticmethod
    def save_file_content(file: str, content: str):
        """
        保存配置到json文件
        """

        with open(file, 'w') as f:
            f.write(content)

    def change_start_bat(self, cmd: str = '', port: str = '9205'):
        """
        修改bat启动脚本
        :param cmd:
        :param port:
        :return:
        """
        self.set('START_BAT', cmd)
        with open(self.cmd_bat_tpl_path, 'r') as f:
            cmd_tpl = f.read()

        new_cmd = cmd_tpl.format(cmd=cmd, port=port)

        with open(self.cmd_bat_path, 'w') as f:
            f.write(new_cmd)
