from django.db import models
# Create your models here.
from django.utils import timezone


class WindowsStat(models.Model):
    tags = models.CharField("标签", max_length=32)
    host = models.CharField("主机ip", max_length=32)
    port = models.IntegerField("winrm端口号", default=5985)
    hostname = models.CharField("主机名", max_length=64, blank=True, null=True)
    osname = models.CharField("主机os名", max_length=64, blank=True, null=True)
    ip_info = models.CharField("IP地址信息", max_length=255, blank=True, null=True)
    windows_version = models.CharField("windows版本", max_length=64, blank=True, null=True)
    updays = models.CharField("启动天数", max_length=255, blank=True, null=True)
    manufacturer = models.CharField("生产商", max_length=64, blank=True, null=True)
    cpu_type = models.CharField("CPU型号", max_length=264, blank=True, null=True)
    cpu_cores = models.CharField("CPU核心数", max_length=64, blank=True, null=True)
    cpu_thread = models.CharField('CPU线程数', max_length=64, blank=True, null=True)
    cpu_speed = models.CharField("CPU频率(HZ)", max_length=512, blank=True, null=True)
    cpu_used_rate = models.FloatField("CPU使用率", blank=True, null=True)
    physical_mem_total = models.FloatField("物理内存总大小(MB)", blank=True, null=True)
    physical_mem_free = models.FloatField('空闲物理内存(MB)', blank=True, null=True)
    physical_mem_used = models.FloatField('已使用物理内存(MB)', blank=True, null=True)
    physical_mem_used_rate = models.FloatField("物理内存使用率", blank=True, null=True)
    virtual_mem_total = models.FloatField('虚拟内存总容量(MB)', blank=True, null=True)
    virtual_mem_free = models.FloatField('虚拟内存空闲(MB)', blank=True, null=True)
    virtual_mem_used = models.FloatField('已使用的虚拟内存(MB)', blank=True, null=True)
    virtual_mem_used_rate = models.FloatField('虚拟内存使用率', blank=True, null=True)
    status = models.IntegerField("windows主机连接状态 0成功 1失败", blank=True, null=True)
    check_time = models.DateTimeField("采集时间", default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'windows_stat'
        verbose_name = "Windows主机采集数据"
        verbose_name_plural = verbose_name


class WindowsStatHis(models.Model):
    tags = models.CharField("标签", max_length=32)
    host = models.CharField("主机ip", max_length=32)
    port = models.IntegerField("winrm端口号", default=5985)
    hostname = models.CharField("主机名", max_length=64, blank=True, null=True)
    osname = models.CharField("主机os名", max_length=64, blank=True, null=True)
    ip_info = models.CharField("IP地址信息", max_length=255, blank=True, null=True)
    windows_version = models.CharField("windows版本", max_length=64, blank=True, null=True)
    updays = models.CharField("启动天数", max_length=255, blank=True, null=True)
    manufacturer = models.CharField("生产商", max_length=64, blank=True, null=True)
    cpu_type = models.CharField("CPU型号", max_length=255, blank=True, null=True)
    cpu_cores = models.CharField("CPU核心数", max_length=64, blank=True, null=True)
    cpu_thread = models.CharField('CPU线程数', max_length=64, blank=True, null=True)
    cpu_speed = models.CharField("CPU频率", max_length=512, blank=True, null=True)
    cpu_used_rate = models.FloatField("CPU使用率", blank=True, null=True)
    physical_mem_total = models.FloatField("物理内存总大小(MB)", blank=True, null=True)
    physical_mem_free = models.FloatField('空闲物理内存(MB)', blank=True, null=True)
    physical_mem_used = models.FloatField('已使用物理内存(MB)', blank=True, null=True)
    physical_mem_used_rate = models.FloatField("物理内存使用率", blank=True, null=True)
    virtual_mem_total = models.FloatField('虚拟内存总容量(MB)', blank=True, null=True)
    virtual_mem_free = models.FloatField('虚拟内存空闲(MB)', blank=True, null=True)
    virtual_mem_used = models.FloatField('已使用的虚拟内存(MB)', blank=True, null=True)
    virtual_mem_used_rate = models.FloatField('虚拟内存使用率', blank=True, null=True)
    status = models.IntegerField("windows主机连接状态 0成功 1失败", blank=True, null=True)
    check_time = models.DateTimeField("采集时间", default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'windows_stat_his'
        verbose_name = "Windows主机采集数据"
        verbose_name_plural = verbose_name


class WindowsDisk(models.Model):
    tags = models.CharField("标签", max_length=32)
    host = models.CharField("主机ip", max_length=32)
    mount_point = models.CharField("挂载点", max_length=256, blank=True, null=True)
    total_size = models.FloatField("总空间大小(GB)", blank=True, null=True)
    used_size = models.FloatField("使用空间大小(GB)", blank=True, null=True)
    free_size = models.FloatField("剩余空间大小(GB)", blank=True, null=True)
    used_percent = models.FloatField("使用率", blank=True, null=True)
    check_time = models.DateTimeField("采集时间", default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'windows_disk'
        verbose_name = "Windows磁盘信息采集数据"
        verbose_name_plural = verbose_name


class WindowsDiskHis(models.Model):
    tags = models.CharField("标签", max_length=32)
    host = models.CharField("主机ip", max_length=32)
    mount_point = models.CharField("挂载点", max_length=256, blank=True, null=True)
    total_size = models.FloatField("总空间大小", blank=True, null=True)
    used_size = models.FloatField("使用空间大小", blank=True, null=True)
    free_size = models.FloatField("剩余空间大小", blank=True, null=True)
    used_percent = models.FloatField("使用率", blank=True, null=True)
    check_time = models.DateTimeField("采集时间", default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'windows_disk_his'
        verbose_name = "Windows磁盘信息采集数据"
        verbose_name_plural = verbose_name
