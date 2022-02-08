import winrm
from datetime import datetime


COMMAND = {
    'hostname': 'hostname',
    'osname': 'wmic os get Caption',
    'ip_info': '''for /f "tokens=2 delims=[]" %a in ('ping -n 1 -4 "%computername%"') do @echo %a''',
    'windows_version': 'ver',
    'start_time': 'wmic path Win32_OperatingSystem get LastBootUpTime',
    'cpu_type': 'wmic cpu get Name',
    'cpu_cores': 'wmic cpu get NumberOfCores',
    'cpu_thread': 'wmic cpu get NumberOfLogicalProcessors',
    'cpu_speed': 'wmic cpu get MaxClockSpeed',
    'cpu_used_rate': 'wmic cpu get loadpercentage',
    'physical_mem_total': 'wmic ComputerSystem get TotalPhysicalMemory',
    'physical_mem_free': 'wmic OS get FreePhysicalMemory',
    'virtual_mem_total': 'wmic os get SizeStoredInPagingFiles',
    'virtual_mem_free': 'wmic os get FreeSpaceInPagingFiles',
    'manufacturer': 'wmic bios get Manufacturer',
    'disk_info': 'wmic volume get Caption, Capacity, freespace'
}


class WindowsStat:
    def __init__(self):
        pass

    def connection(self, windows_tag, windows_params):
        """
        连接winrm
        """
        print(f'开始获取：{windows_tag}的相关信息')
        # 创建winrm连接对象
        session = winrm.Session('http://' + windows_params['host'] + ':' + str(windows_params['port']) + '/wsman',
                                auth=(windows_params['username'], windows_params['password']))
        return session

    def get_info(self, windows_tag, windows_params):
        """
        获取所有信息
        """
        try:
            session = self.connection(windows_tag, windows_params)
            # 测试服务器连接是否正常
            self.run_cmd(session, ' ')
        except Exception as e:
            print(e)
            print('windows服务器连接超时！')
            return None, None
        host_info = self.get_host_info(session)
        # print(host_info)
        cpu_info = self.get_cpu_info(session)
        # print(cpu_info)
        mem_info = self.get_mem_info(session)
        # print(mem_info)
        disk_info = self.get_disk_info(session)

        return {**host_info, **cpu_info, **mem_info}, disk_info

    def run_cmd(self, session, command):
        """
        在此执行命令
        """
        data = session.run_cmd(command).std_out
        # print(data)
        return data

    def get_host_info(self, session):
        """
        主机相关信息
        """
        hostname = self.run_cmd(session, COMMAND['hostname']).decode('gbk').strip()
        osname = '-'.join(self.run_cmd(session, COMMAND['osname']).decode('gbk').split())
        ip_info = self.run_cmd(session, COMMAND['ip_info']).decode('gbk').strip()
        windows_version = self.run_cmd(session, COMMAND['windows_version']).decode('gbk').strip()
        start_time = datetime.strptime(
                self.run_cmd(session, COMMAND['start_time']).decode('gbk').split()[1].split('.')[0],
                '%Y%m%d%H%M%S'
            )
        manufacturer = self.run_cmd(session, COMMAND['manufacturer']).decode('gbk').split()[1]
        return {
            'hostname': hostname,
            'osname': osname,
            'ip_info': ip_info,
            'windows_version': windows_version,
            'start_time': start_time,
            'manufacturer': manufacturer,
        }

    def get_cpu_info(self, session):
        """
        获取cpu相关信息
        """
        cpu_type = ' '.join(self.run_cmd(session, COMMAND['cpu_type']).decode('gbk').split()[1:])
        cpu_cores = self.run_cmd(session, COMMAND['cpu_cores']).decode('gbk').split()[1:][0]
        cpu_thread = self.run_cmd(session, COMMAND['cpu_thread']).decode('gbk').split()[1:][0]
        cpu_speed = self.run_cmd(session, COMMAND['cpu_speed']).decode('gbk').split()[1:][0]
        cpu_used_rate = self.run_cmd(session, COMMAND['cpu_used_rate']).decode('gbk').split()[1:][0]

        return {
            'cpu_type': cpu_type,
            'cpu_cores': cpu_cores,
            'cpu_thread': cpu_thread,
            'cpu_speed': cpu_speed,
            'cpu_used_rate': round(float(cpu_used_rate), 2)

        }

    def get_mem_info(self, session):
        """
        获取内存相关信息
        """
        physical_mem_total = self.run_cmd(session, COMMAND['physical_mem_total']).decode('gbk').split()[1]
        physical_mem_free = self.run_cmd(session, COMMAND['physical_mem_free']).decode('gbk').split()[1]
        virtual_mem_total = self.run_cmd(session, COMMAND['virtual_mem_total']).decode('gbk').split()[1]
        virtual_mem_free = self.run_cmd(session, COMMAND['virtual_mem_free']).decode('gbk').split()[1]

        return {
            'physical_mem_total': round(float(physical_mem_total) / 1024 / 1024, 2),
            'physical_mem_free': round(float(physical_mem_free) / 1024, 2),
            'virtual_mem_total': round(float(virtual_mem_total) / 1024, 2),
            'virtual_mem_free': round(float(virtual_mem_free) / 1024, 2),
        }

    def get_disk_info(self, session):
        disk_info = self.run_cmd(session, COMMAND['disk_info']).decode('gbk').split()
        to_delete_disk_info = []
        for k, v in enumerate(disk_info):
            if v.startswith(r'\\'):
                # print(k, v)
                to_delete_disk_info += disk_info[k-1:k + 2]
        disk_info = [item for item in disk_info if item not in to_delete_disk_info]
        disk_dict = {}
        for i in range(1, len(disk_info) // 3):
            # disk_dict[data[4]] =
            disk_dict[disk_info[1 + 3 * i]] = {
                'Capacity': disk_info[3 * i],
                'FreeSpace': disk_info[1 + 3 * i + 1]
            }
        return disk_dict















































