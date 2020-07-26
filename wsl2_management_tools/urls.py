# ==================================================================
#       文 件 名: urls.py
#       概    要: 
#       作    者: IT小强 
#       创建时间: 2020/7/25 12:41
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='get_port_info'),
    path('del_port_wall_all/', views.del_port_wall_all, name='del_port_wall_all'),
    path('add_port_wall_all/', views.add_port_wall_all, name='add_port_wall_all'),
    path('update_port_wall_all/', views.update_port_wall_all, name='update_port_wall_all'),
]
