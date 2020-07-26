# ==================================================================
#       文 件 名: windows_command.py
#       概    要: Windows命令处理
#       作    者: IT小强 
#       创建时间: 2020/7/26 11:25
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import os
import re


class WindowsCommand:
    """

    """

    bash = r'bash.exe'

    wsl_exe = r'wsl.exe'

    power_shell = r'PowerShell.exe'

    @staticmethod
    def run_cmd(cmd: str):
        return os.popen(cmd).read()


class WindowsCommandWSL2(WindowsCommand):
    """
    WSL2管理
    """

    cmd_get_wsl_info = '{wsl_exe} -l -v'

    cmd_get_wsl_ip = '{bash} -c "ifconfig eth0 | grep \'inet \'"'

    @classmethod
    def get_wsl_ip(cls) -> str:
        """
        该方法用于获取WSL2的IP
        :return: str
        """

        pattern: str = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        cmd = cls.cmd_get_wsl_ip.format(bash=cls.bash)

        try:
            result = cls.run_cmd(cmd)
            wsl_ip = re.search(pattern, result).group(0)
        except AttributeError:
            wsl_ip = ''
        return wsl_ip

    @classmethod
    def get_wsl_info(cls, return_str: bool = False):
        """
        获取wsl信息
        :param return_str: 是否返回字符串，否则返回列表格式
        :return:
        """

        cmd = cls.cmd_get_wsl_info.format(wsl_exe=cls.wsl_exe)
        info_str = cls.run_cmd(cmd)
        if not return_str:
            return cls.wsl_info_to_list(info_str)
        return info_str

    @staticmethod
    def wsl_info_to_list(info_str: str) -> list:
        """
        格式化WSL信息
        :param info_str:
        :return: 以字典形式返回
        """
        info = []
        for line in info_str.splitlines():
            line = line.replace('\x00', '').strip().split()
            if line:
                if line[0] == 'NAME' and line[1] == 'STATE' and line[2] == 'VERSION':
                    continue
                is_default = line[0] == '*'
                if is_default:
                    line = line[1:]
                info.append({
                    'name': line[0],
                    'state': line[1],
                    'version': line[2],
                    'is_default': is_default,
                })
        return info


class WindowsCommandPort(WindowsCommand):
    """
    端口转发管理
    """

    port_pre = '{power_shell} netsh interface portproxy '

    cmd_port_add = port_pre + 'add v4tov4 listenport={port} listenaddress={addr} connectport={port} connectaddress={ip}'

    cmd_port_del = port_pre + 'delete v4tov4 listenport={port} listenaddress={addr}'

    cmd_port_info = '{power_shell} netsh interface portproxy show all'

    @classmethod
    def add_port(cls, port: int, addr: str = '0.0.0.0', ip: str = '') -> str:
        """
        添加端口转发
        :param addr: 监听地址
        :param ip: 待转发的IP地址
        :param port: 待添加端口号
        :return:
        """

        if not ip:
            ip = WindowsCommandWSL2.get_wsl_ip()

        if not ip:
            return ''

        cmd = cls.cmd_port_add.format(
            power_shell=cls.power_shell,
            port=port,
            addr=addr,
            ip=ip
        )

        return cls.run_cmd(cmd)

    @classmethod
    def del_port(cls, port: int, addr: str = '0.0.0.0') -> str:
        """
        删除端口转发
        :param addr: 监听地址
        :param port: 待删除的端口号
        :return:
        """

        cmd = cls.cmd_port_del.format(
            power_shell=cls.power_shell,
            port=port,
            addr=addr,
        )

        return cls.run_cmd(cmd)

    @classmethod
    def get_port_info(cls, return_str: bool = False):
        """
        获取端口转发信息
        :param return_str: 是否返回字符串，否则返回列表格式
        :return:
        """

        cmd = cls.cmd_port_info.format(power_shell=cls.power_shell)
        info_str = cls.run_cmd(cmd)
        if not return_str:
            return cls.port_info_to_list(info_str)
        return info_str

    @staticmethod
    def port_info_to_list(info_str: str) -> list:
        """
        格式化端口信息
        :param info_str:
        :return: 以字典形式返回
        """

        info = []
        pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*?)(\d+)(.*?)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        for line in info_str.splitlines():
            line_info = re.search(pattern, line)
            if line_info:
                info.append({
                    'addr': line_info.group(1),
                    'port': line_info.group(3),
                    'ip': line_info.group(5),
                })
        return info


class WindowsCommandFireWall(WindowsCommand):
    """
    防火墙管理
    """

    FIRE_WALL_RULE_OUT = 'Outbound'

    FIRE_WALL_RULE_IN = 'Inbound'

    wall_name = 'WSL 2 Firewall Unlock'

    cmd_wall_add = "{power_shell} New-NetFireWallRule -DisplayName '{wall_name}' -Direction '{wall_type}' -LocalPort {port} -Action Allow -Protocol TCP"

    cmd_wall_del = "{power_shell} Remove-NetFireWallRule -DisplayName '{wall_name}'"

    @classmethod
    def add_wall(cls, port: int, wall_types: list = None) -> str:
        """
        添加防火墙规则
        :param port: 端口号
        :param wall_types: 防火墙类型 ['Outbound','Inbound']
        :return:
        """

        return cls._wall(cls.cmd_wall_add, port, wall_types)

    @classmethod
    def del_wall(cls, port: int, wall_types: list = None) -> str:
        """
        删除防火墙规则
        :param port: 端口号
        :param wall_types: 防火墙类型 ['Outbound','Inbound']
        :return:
        """

        return cls._wall(cls.cmd_wall_del, port, wall_types)

    @classmethod
    def _wall(cls, wall_cmd: str, port: int, wall_types: list = None) -> str:
        """
        防火墙操作
        :param port: 端口号
        :param wall_types: 防火墙类型 ['Outbound','Inbound']
        :return:
        """

        default_wall_types = [cls.FIRE_WALL_RULE_IN, cls.FIRE_WALL_RULE_OUT]

        if not wall_types:
            wall_types = default_wall_types

        result = ''

        for wall_type in wall_types:
            if wall_type not in default_wall_types:
                continue
            cmd = wall_cmd.format(
                wall_group=cls.wall_name,
                wall_name='{name} {port} {type}'.format(name=cls.wall_name, port=port, type=wall_type),
                power_shell=cls.power_shell,
                port=port,
                wall_type=wall_type,
            )
            result += cls.run_cmd(cmd)

        return result


def add_port_wall(port: int, addr: str = '0.0.0.0', wall_types: list = None, ip: str = ''):
    """
    添加端口转发并开放防火墙
    :param port: 待添加端口号
    :param ip: 待转发的IP地址
    :param addr: 监听地址
    :param wall_types: 防火墙类型 ['Outbound','Inbound']
    :return:
    """

    return WindowsCommandPort.add_port(port, addr, ip) + WindowsCommandFireWall.add_wall(port, wall_types)


def del_port_wall(port: int, addr: str = '0.0.0.0', wall_types: list = None):
    """
    删除端口转发并删除防火墙
    :param port: 待添加端口号
    :param addr: 监听地址
    :param wall_types: 防火墙类型 ['Outbound','Inbound']
    :return:
    """

    return WindowsCommandPort.del_port(port, addr) + WindowsCommandFireWall.del_wall(port, wall_types)


def add_port_wall_all(ports, addr: str = '0.0.0.0', wall_types: list = None, ip: str = ''):
    """
    添加端口转发并开放防火墙
    :param ports: 待添加端口号列表
    :param ip: 待转发的IP地址
    :param addr: 监听地址
    :param wall_types: 防火墙类型 ['Outbound','Inbound']
    :return:
    """

    if isinstance(ports, str):
        ports = ports.split(',')

    result = ''
    for port in ports:
        result += add_port_wall(port, addr, wall_types, ip)
    return result


def del_port_wall_all(ports, addr: str = '0.0.0.0', wall_types: list = None):
    """
    删除端口转发并删除防火墙
    :param ports: 待添加端口号列表
    :param addr: 监听地址
    :param wall_types: 防火墙类型 ['Outbound','Inbound']
    :return:
    """

    if isinstance(ports, str):
        ports = ports.split(',')

    result = ''
    for port in ports:
        result += del_port_wall(port, addr, wall_types)
    return result
