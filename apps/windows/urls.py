from django.urls import path
from django.conf.urls import url
from windows import views

app_name = "windows"

urlpatterns = [
    path('api/windows-stat-list', views.ApiWindowsStatList.as_view()),
    path('api/windows-stat', views.ApiWindowsStat.as_view()),
    path('api/windows-stat-his', views.ApiWindowsStatHis.as_view()),
    path('api/windows-disk', views.ApiWindowsDisk.as_view()),
    url(r'api/del_windows_stat/(?P<host>.*)', views.del_windows_stat)
]

