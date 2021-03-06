from django.urls import path
from django.conf.urls import url
from linux import views

app_name = "linux"

urlpatterns = [
    path('api/linux-stat-list', views.ApiLinuxStatList.as_view()),
    path('api/linux-stat', views.ApiLinuxStat.as_view()),
    path('api/linux-stat-his', views.ApiLinuxStatHis.as_view()),
    path('api/linux-disk', views.ApiLinuxDisk.as_view()),
    path('api/linux-disk-his', views.ApiLinuxDiskHis.as_view()),
    path('api/linux-io-stat', views.ApiLinuxIoStat.as_view()),
    path('api/linux-io-stat-his', views.ApiLinuxIoStatHis.as_view()),
    url(r'^api/del_linux_stat/(?P<host>.*)', views.del_linux_stat)
]

