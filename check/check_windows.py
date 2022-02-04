from pprint import pprint
from datetime import datetime

from utils.tools import mysql_exec, now, clear_table, archive_table

from check.windows_stat import WindowsStat


def check_windows(windows_tag, windows_params):
    default_windows_stat, default_windows_disk = WindowsStat().get_info(windows_tag, windows_params)
    # pprint(default_windows_stat)
    # pprint(default_windows_disk)
    if default_windows_stat and default_windows_disk:
        # 获取到windows状态相关逻辑
        # 计算已使用物理内存
        physical_mem_used = round(default_windows_stat['physical_mem_total'] - default_windows_stat['physical_mem_free'], 2)
        # 计算物理内存使用率
        physical_mem_used_rate = round((physical_mem_used / default_windows_stat['physical_mem_total']) * 100, 2)
        # 计算已使用的虚拟内存
        virtual_mem_used = round(default_windows_stat['virtual_mem_total'] - default_windows_stat['virtual_mem_free'], 2)
        # 计算虚拟内存使用率
        virtual_mem_used_rate = round((virtual_mem_used / default_windows_stat['virtual_mem_total']) * 100, 2)

        # 需要拼接windows_stat
        other_windows_stat = {
            'tags': windows_tag,
            'port': windows_params['port'],
            'host': windows_params['host'],
            'updays': (datetime.now() - default_windows_stat['start_time']).__str__().split('.')[0],
            'physical_mem_used': physical_mem_used,
            'physical_mem_used_rate': physical_mem_used_rate,
            'virtual_mem_used': virtual_mem_used,
            'virtual_mem_used_rate': virtual_mem_used_rate,
            'status': 0,
            'check_time': datetime.now(),
        }
        # pprint({**default_windows_stat, **other_windows_stat})
        # 1.清除windows_stat中当前tag的数据
        clear_table(windows_tag, 'windows_stat')
        # 1.1将获取到的windows_stat存入到数据库中
        insert_sql_windows_stat = """
        insert into windows_stat(
        tags, host, port, hostname, osname, ip_info, windows_version, updays, cpu_type, cpu_cores, cpu_thread,
        cpu_speed, cpu_used_rate, physical_mem_total, physical_mem_free, physical_mem_used, physical_mem_used_rate, 
        virtual_mem_total, virtual_mem_free, virtual_mem_used,virtual_mem_used_rate, status, check_time, manufacturer 
        )
        values(
        '{tags}', '{host}', {port}, '{hostname}', '{osname}', '{ip_info}', '{windows_version}', '{updays}', 
        '{cpu_type}', '{cpu_cores}', '{cpu_thread}', '{cpu_speed}', {cpu_used_rate}, {physical_mem_total}, 
        {physical_mem_free}, {physical_mem_used}, {physical_mem_used_rate}, {virtual_mem_total}, 
        {virtual_mem_free}, {virtual_mem_used}, {virtual_mem_used_rate}, {status}, '{check_time}', '{manufacturer}' 
        )
        """
        windows_stat = {**default_windows_stat, **other_windows_stat}
        insert_sql = insert_sql_windows_stat.format(**windows_stat)
        print('插入到windows_stat表中', insert_sql)
        mysql_exec(insert_sql)
        # 1.2将windows_stat备份到windows_stat_his表中
        archive_table(windows_tag, 'windows_stat')

        # 2.清除windows_disk中当前tag的数据
        clear_table(windows_tag, 'windows_disk')
        # 2.1将获取到的windows_disk存入到数据库中
        insert_sql_windows_disk = """
        insert into windows_disk(
        tags, host, mount_point, total_size, used_size, free_size, used_percent, check_time
        )
        values(
        '{tags}', '{host}', '{mount_point}', {total_size}, {used_size}, {free_size}, {used_percent}, '{check_time}'
        )
        """
        for mount_point, value in default_windows_disk.items():
            total_size = round(int(value['Capacity']) / 1024 / 1024 / 1024, 2)
            free_size = round(int(value['FreeSpace']) / 1024 / 1024 / 1024, 2)
            used_size = round(total_size - free_size, 2)
            used_percent = round(used_size / total_size * 100, 2)
            windows_disk = {
                'tags': windows_tag,
                'host': windows_params['host'],
                'mount_point': mount_point[0:2],
                'total_size': total_size,
                'free_size': free_size,
                'used_size': used_size,
                'used_percent': used_percent,
                'check_time': datetime.now()
            }
            insert_sql = insert_sql_windows_disk.format(**windows_disk)
            print('插入到windows_disk表中', insert_sql)
            mysql_exec(insert_sql)
        # 2.2将windows_disk备份到windows_disk_his表中
        archive_table(windows_tag, 'windows_disk')
    else:
        # 连接错误相关逻辑
        print('windows服务器连接失败！')
        clear_table(windows_tag, 'windows_stat')
        insert_sql_data = """
        insert into windows_stat(tags, host, port, status, check_time)
        values('{tags}', '{host}', {port}, {status}, '{check_time}')
        """
        insert_sql_value = {
            'tags': windows_tag,
            'port': windows_params['port'],
            'host': windows_params['host'],
            'status': 1,
            'check_time': datetime.now(),
        }
        insert_sql = insert_sql_data.format(**insert_sql_value)
        mysql_exec(insert_sql)
        archive_table(windows_tag, 'windows_stat')


if __name__ == '__main__':
    tag = 'test'
    params = {
        'host': '192.168.1.6',
        # 'host': '123.168.1.6',
        'port': 5985,
        'username': 'system-user',
        'password': '1234'
    }
    # check_windows(tag, params)

