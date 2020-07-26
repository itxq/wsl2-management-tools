from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from . import windows_command


def add_port_wall_all(request):
    ports = request.GET.get('ports', '')
    windows_command.add_port_wall_all(ports=ports)
    return HttpResponseRedirect(reverse('get_port_info'))


def del_port_wall_all(request):
    ports = request.GET.get('ports', '')
    windows_command.del_port_wall_all(ports=ports)
    return HttpResponseRedirect(reverse('get_port_info'))


def update_port_wall_all(request):
    ports = request.GET.get('ports', '')
    windows_command.del_port_wall_all(ports=ports)
    windows_command.add_port_wall_all(ports=ports)
    return HttpResponseRedirect(reverse('get_port_info'))


def index(request):
    port_info = windows_command.WindowsCommandPort.get_port_info()
    wsl_ip = windows_command.WindowsCommandWSL2.get_wsl_ip()
    wsl_info = windows_command.WindowsCommandWSL2.get_wsl_info()

    return render(request, 'wsl2_management_tools/port.html', {
        'ports': port_info,
        'wsl_ip': wsl_ip,
        'wsl_info': wsl_info,
        'base_dir': settings.BASE_DIR,
        'start_bat': settings.SETTINGS_MANAGE.get('START_BAT', ''),
        'python_path': settings.SETTINGS_MANAGE.get('PYTHON_PATH', ''),
        'server_port': settings.SETTINGS_MANAGE.get('SERVER_PORT', ''),
    })


def change_start_bat(request):
    """
    修改启动脚本
    :param request:
    :return:
    """

    cmd = str(request.GET.get('cmd', ''))
    port = str(request.GET.get('port', settings.SETTINGS_MANAGE.get('SERVER_PORT')))
    python_path = str(request.GET.get('python_path', settings.SETTINGS_MANAGE.get('PYTHON_PATH')))

    settings.SETTINGS_MANAGE.change_start_bat(
        cmd=cmd,
        port=port,
        python_path=python_path
    )

    return HttpResponseRedirect(reverse('get_port_info'))
