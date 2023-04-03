import paramiko

aa = ""
bb = "192.168.0.300"
cc = aa + (',' if (aa and bb) else '') + bb
print(cc)

# class SSHClient:
#     def __init__(self, hostname, username, password):
#         self.hostname = hostname
#         self.username = username
#         self.password = password
#         self.ssh = None
    
#     def connect(self):
#         self.ssh = paramiko.SSHClient()
#         self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
    
#     def execute_command(self, command):
#         stdin, stdout, stderr = self.ssh.exec_command(command)
#         output = stdout.read().decode('utf-8')
#         k3sproc = stdout.channel.recv_exit_status()
#         return output, k3sproc
    
#     def close(self):
#         if self.ssh:
#             self.ssh.close()

# mhosts = '192.168.0.146,192.168.0.160'

# for i in mhosts:
#     ssh_client = SSHClient(i, username, password)
#     ssh_client.connect()
#     k3sproc = ssh_client.execute_command('pgrep -l k3s | wc -l', timeout=5)
#     k3status = k3sproc.readlines()
#     num_processes = int(k3status[0])
#     if num_processes == 1:
#         output = ssh_client.execute_command('sudo k3s-uninstall.sh')
#         print(output)
#         ssh_client.close()
#     else:
#         continue
# # for i in whosts:
# #     ssh_client = SSHClient(i, username, password)
# #     ssh_client.connect()
# #     output = ssh_client.execute_command('sudo k3s-agent-uninstall.sh')
# #     print(output)
# #     ssh_client.close()
# # result['changed'] = True
# # result['k3s_state'] = 'Destroyed'