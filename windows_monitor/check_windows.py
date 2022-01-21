import winrm
import wmi


session = winrm.Session('http://47.106.222.28:5985/wsman', auth=(r'administrator', 'fdy12345678.'))
res = session.run_cmd(''' ipconfig ''')
status_code = res.status_code
print('状态码:', status_code)
data = res.std_out.decode('gbk')
# print(data.split())
print('返回值:', data, type(data))
# print(res.std_err)



