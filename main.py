import paramiko

command = "curl -sfL https://get.k3s.io | sh -"

# Update the next three lines with your
# server's information

host = "192.168.0.146"
username = "aya"
password = "tgo090393"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command("curl -sfL https://get.k3s.io | sh -")
print(_stdout.read().decode())
client.close()