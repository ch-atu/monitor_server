from pprint import pprint
from datetime import datetime

from utils.tools import mysql_exec, now, clear_table, archive_table

from check.windows_stat import WindowsStat


def check_windows(windows_tag, windows_params):
    default_windows_stat = WindowsStat().get_info(windows_tag, windows_params)
    if default_windows_stat:
        # 获取到windows状态相关逻辑
        # 计算已使用物理内存
        physical_mem_used = round(default_windows_stat['physical_mem_total'] - default_windows_stat['physical_mem_free'], 2)
        # 计算物理内存使用率
        physical_mem_used_rate = round((physical_mem_used / default_windows_stat['physical_mem_total']) * 100, 2)
        # 计算已使用的虚拟内存
        virtual_mem_used = round(default_windows_stat['virtual_mem_total'] - default_windows_stat['virtual_mem_free'], 2)
        # 计算虚拟内存使用率
        virtual_mem_used_rate = round((virtual_mem_used / default_windows_stat['virtual_mem_total']) * 100, 2)

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
        # 清除windows_stat中当前tag的数据
        clear_table(windows_tag, 'windows_stat')
        # 将获取到的windows_stat存入到数据库中
        insert_sql_data = """
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
        insert_sql_value = {**default_windows_stat, **other_windows_stat}
        insert_sql = insert_sql_data.format(**insert_sql_value)
        print(insert_sql)
        # 将windows_stat备份到windows_stat_his表中
        mysql_exec(insert_sql)
        archive_table(windows_tag, 'windows_stat')
    else:
        # 连接错误相关逻辑
        print('服务器连接失败！')
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
        'host': '192.168.16.155',
        'port': 5985,
        'username': 'system-user',
        'password': '1234'
    }
    check_windows(tag, params)
