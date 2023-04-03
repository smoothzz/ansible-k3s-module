#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import paramiko
import secrets
from multiprocessing import Pool

class SSHClient:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh = None
    
    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
    
    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        # k3sproc = stdout.channel.recv_exit_status()
        return output
    # k3sproc    
    def close(self):
        if self.ssh:
            self.ssh.close()

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        calico=dict(type='str', required=False),
        traefik=dict(type='bool', required=False, default=True),
        configure_host=dict(type='bool', required=False, default=False),
        autoGen_token=dict(type='bool', required=False, default=False),
        master_hosts=dict(type='str', required=False),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        worker_hosts=dict(type='str', required=False),
        servicelb=dict(type='bool', required=False, default=True),
        whatdo=dict(type='str', required=False, default='provision')
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        k3s_state=''
    )
    
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    ### Module helpers ###
    token = secrets.token_hex(32)
    mhosts = module.params['master_hosts']
    whosts = module.params['worker_hosts']
    username = module.params['username']
    password = module.params['password']

    if module.params['whatdo'] == 'provision':
        look_k3s = mhosts + ',' + whosts
        for i in look_k3s.split(','):
            ssh_client = SSHClient(i, username, password)
            ssh_client.connect()
            k3sproc = ssh_client.execute_command('pgrep -l k3s | wc -l')
            num_processes = int(k3sproc[0])
            if num_processes == 1:
                module.fail_json(msg=f'Host {i} has service k3s up, fix and restart the process.', **result)
        if whosts and len(mhosts.split(',')) == 1:
            ssh_client = SSHClient(mhosts.split(',')[0], username, password)
            ssh_client.connect()
            output = ssh_client.execute_command(f'curl -sfL https://get.k3s.io | sh -s - --token {token}')
            print(output)
            ssh_client.close()
            for i in whosts.split(','):
                ssh_client = SSHClient(i, username, password)
                ssh_client.connect()
                output = ssh_client.execute_command(f'curl -sfL https://get.k3s.io | K3S_URL=https://{mhosts}:6443 sh -s - agent --token {token}')
                ssh_client.close()
            result['changed'] = True
            result['k3s_state'] = 'Created'
            result['token'] = f'{token}'
        if len(mhosts.split(',')) > 1 and whosts:
            ssh_client = SSHClient(mhosts.split(',')[0], username, password)
            ssh_client.connect()
            output = ssh_client.execute_command(f'curl -sfL https://get.k3s.io | sh -s - server --token {token} --cluster-init') 
            print(output)
            ssh_client.close()
            first_master = mhosts.split(',')[0]
            for i in mhosts.split(',')[1:]:
                ssh_client = SSHClient(i, username, password)
                ssh_client.connect()
                output = ssh_client.execute_command(f'curl -sfL https://get.k3s.io | sh -s - server --token {token} --server https://{first_master}:6443')
                print(output)
                ssh_client.close()
            for i in whosts.split(','):
                ssh_client = SSHClient(i, username, password)
                ssh_client.connect()
                output = ssh_client.execute_command(f'curl -sfL https://get.k3s.io | sh -s - agent --token {token} --server https://{first_master}:6443')
                ssh_client.close()
            result['changed'] = True
            result['k3s_state'] = 'Created'
            result['token'] = f'{token}'

    if module.params['whatdo'] == 'destroy':
        for i in mhosts.split(','):
            ssh_client = SSHClient(i, username, password)
            ssh_client.connect()
            k3sproc = ssh_client.execute_command('pgrep -l k3s | wc -l')
            num_processes = int(k3sproc[0])
            if num_processes == 1:
                output = ssh_client.execute_command('sudo k3s-uninstall.sh')
                print(output)
                ssh_client.close()
            else:
                continue
        for i in whosts.split(','):
            ssh_client = SSHClient(i, username, password)
            ssh_client.connect()
            output = ssh_client.execute_command('sudo k3s-agent-uninstall.sh')
            print(output)
            ssh_client.close()
        result['changed'] = True
        result['k3s_state'] = 'Destroyed'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
