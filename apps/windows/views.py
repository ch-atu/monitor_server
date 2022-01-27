from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *
from utils.tools import get_utctime, today, last_day
from utils.django_tools import NoPagination


class ApiWindowsStat(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        return WindowsStat.objects.filter(status=0, tags=tags).order_by('status')

    serializer_class = WindowsStatSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)


class ApiWindowsStatHis(generics.ListCreateAPIView):
    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)
        if start_time and end_time:
            start_time = get_utctime(start_time)
            end_time = get_utctime(end_time)
        else:
            # default data of 1 day
            end_time = today()
            start_time = last_day()
        return WindowsStatHis.objects.filter(tags=tags, check_time__gte=start_time, check_time__lte=end_time).order_by(
            'check_time')

    serializer_class = WindowsStatHisSerializer
    pagination_class = NoPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.DjangoModelPermissions,)


# all instance
class ApiWindowsStatList(generics.ListCreateAPIView):
    # queryset = LinuxStat.objects.get_queryset().order_by('-status')
    # 模糊查询
    def get_queryset(self):
        host = self.request.query_params.get('host', None)
        if not host:
            return WindowsStat.objects.all().order_by('id')
        hosts = WindowsStat.objects.filter(host__contains=host).order_by('id')
        return hosts
    serializer_class = WindowsStatSerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('tags', 'host', 'status')
    # search_fields = ('tags', 'host',)
    permission_classes = (permissions.DjangoModelPermissions,)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import WindowsStat

@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def del_windows_stat(request,host):
    windows_stat = WindowsStat.objects.filter(host=host)
    windows_stat.delete()
    return Response({
        'message': 'success'
    })

