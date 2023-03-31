import paramiko

command = "curl -sfL https://get.k3s.io | sh -"

# Update the next three lines with your
# server's information

host = "192.168.0.146,192.168.0.50,192.168.0.60,192.168.0.70,192.168.0.80,192.168.0.90,192.168.0.100,192.168.0.146,192.168.0.146"
username = "aya"
password = "123456"

master = host.split(',')
teste = host.split(',')[0]
teste2 = host.split(',')[1:]
count = len(master)

for i in host.split(',')[1:]:
    print(i)

# if len(host.split(',')) >= 2:
#     print('maior que ou igual a 2')
# else:
#     print('menor que 2')

# print(count)

# client = paramiko.client.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(host, username=username, password=password)
# command = "pgrep -x 'k3s'"
# _stdin, _stdout,_stderr = client.exec_command(command)
# output = _stdout.read().decode()
# if output.strip():  # If the output is not empty
#     # The process is running
#     print("The process is running")
# else:
#     # The process is not running
#     print("The process is not running")
# client.close()