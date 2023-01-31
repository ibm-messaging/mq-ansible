# *MQ-Ansible*

| :memo:        | Interested in contributing to this project? Please read our [IBM Contributor License Agreement](CLA.md) and our [Contributing Guide](CONTRIBUTING.md).       |
|---------------|:------------------------|

A collection for automating the installation and configuration of IBM MQ using Ansible on Ubuntu machines. Our aim is to make MQ-Ansible extensible for other platforms and more detailed IBM MQ configuration.

This directory contains:
- ansible [`roles`](https://github.com/ibm-messaging/mq-ansible/tree/main/ansible_collections/ibm/ibmmq/roles) for the installation and configuration of IBM MQ.
- module [`queue_manager.py`](ansible_collections/ibm/ibmmq/library/queue_manager.py) to create and configure a queue manager.
- playbook [`ibmmq.yml`](ansible_collections/ibm/ibmmq/ibmmq.yml) which implements the roles and module.

For a detailed explanation and documentation on how MQ-Ansible works, click [here](https://github.com/ibm-messaging/mq-ansible/wiki).

## Requirements

- `ansible` and `ansible-lint` are required on your local machine to run playbooks implementing this collection.
- An Ubuntu target machine is required to run MQ.

## Roles for IBM MQ installation

The roles in this collection carryout an installation of IBM MQ Advanced on an Ubuntu target machine. The roles have been implemented to set up the required users on the machine, download the software, install and configure IBM MQ, copy over a configurable `dev-config.mqsc` file ready to be run on the target machine, and setup and start the web console. Developers can change this file to allow better configuration of their queue managers.


### Example

```yaml
- hosts: [YOUR_TARGET_MACHINES]
  become: false
  environment:
    PATH: /opt/mqm/bin:{{ ansible_env.PATH }}

  roles: 
    - role: setupusers
      vars:
        gid: 989
    - downloadmq
    - installmq
    - getconfig
    - setupconsole
    - startconsole
```

## Modules for IBM MQ resources' configuration

- `queue_manager.py`- Creates, starts, deletes an IBM MQ queue manager and runs an MQSC file. See the documentation [here.](QUEUE_MANAGER.md)

# Run our sample playbook

### Setup (inventory.ini)

##### Note: *Ansible* must be installed on the local machine. ([Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

Before running the playbook implementing our modules and roles for IBM MQ:

1. Check if you have an *ssh* key pair in order to access the target machines via Ansible. Go to the `~/.ssh` directory in your machine and look for the `id_rsa` and `id_rsa.pub` files.

    ```shell
     cd ~/.ssh
    ```

2. If those two files are not in your `ssh` directory, you need to generate `id_rsa` and `id_rsa.pub` with the following command:

    ```shell
     ssh-keygen
    ```

3. Once the keys have been generated, these need to be copied to the target machine's user `ssh` directory. 

    ```shell
     ssh-copy-id -i id_rsa.pub [USER]@[YOUR_TARGET_MACHINE_IP]
    ```
    
4. To confirm the keys have been copied successfully, connect to your target machine by:

    ```shell
     ssh [USER]@[YOUR_TARGET_MACHINE_IP]
    ```
    This should connect to your target machine without asking for a password.
    
5. Go to the `ansible_collections/ibm/ibmmq/` directory.

    ```shell
     cd ..
     cd ansible_collections/ibm/ibmmq/
    ```


6. Create a file `inventory.ini` inside the directory with the following content:
  
    ```ini
    
    [servers]
    server-alias-n ansible_host=[YOUR_HOSTNAME_n] ansible_ssh_user=[YOUR_SSH_USER]
    server-alias-n ansible_host=[YOUR_HOSTNAME_n] ansible_ssh_user=[YOUR_SSH_USER]

    ```
   - Change each `server-alias-n` to an alias name that you wish to use
   - Change each `YOUR_HOSTNAME_n` to your server/hostname, for example: `myserver-1.fyre.com`.
   - Change `YOUR_SSH_USER` to your target machine's SSH user.
   ##### *NOTE* : the user on the target machine MUST have `sudo` privileges.

### ibmmq.yml

The sample playbook [`ibmmq.yml`](ansible_collections/ibm/ibmmq/ibmmq.yml) installs IBM MQ Advanced with our roles and configures a queue manager with the `queue_manager.py` module.

1. Before running the playbook, ensure that you have added the directory path to the PATH environment variable.

    ##### *NOTE* : change `<PATH-TO>` to your local directory path:

    - On Mac:

          ```shell
           export ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY}:<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
          ```

    - On Windows: 

          ```shell
           set ANSIBLE_LIBRARY=%ANSIBLE_LIBRARY%;<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
          ```

2. Run the following command to execute the tasks within the playbook:
      ```shell
       ansible-playbook ./ibmmq.yml -i inventory.ini [-K]
      ```
      - ##### *NOTE* : `-K` will prompt the user to enter the sudo password for [YOUR_SSH_USER] on the target machine, you can omit if you have setup SSH keys.

3. The playbook should return the result of `dspmq` with the queue manager created listed. Log into your target machine and check it manually:

    ```shell
     dspmq
    ```

# Troubleshooting

If one of the following errors appears during the run of the playbook, run the following commands according to the problem:

- `Please add this host's fingerprint to your known_hosts file to manage this host.` - Indicates that an SSH password cannot be used instead of a key. 
  
  Fix:
    ##### *NOTE* : change `[YOUR_MACHINE_IP]` to the target machine's public IP address
  ```shell
  ssh-keyscan -H [YOUR_MACHINE_IP] >> ~/.ssh/known_hosts
  ```
- `zsh: command not found: dspmq` - Appears that MQ environment variables have not been set.

  Fix:
  ```shell
  . /opt/mqm/bin/setmqenv -s
  ```
- `AMQ7077E: You are not authorized to perform the requested operation` - Appears that the user cannot carry out queue manager operations. This occurs when an SSH session to a target machine hasn't been refreshed after the roles have been executed.
  
  Fix:

  Restart the SSH session.


# Testing framework

### Testing module's functionality with playbooks

These playbooks test the functionality and performance of our roles and the queue_manager module in Ansible plays.

To run the test playbooks first:

1. make sure you are in the right directory 
    ```shell
     cd tests/playbooks
    ```
2. export the modules to your Ansible library
    ```shell
     export ANSIBLE_LIBRARY=<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
    ```
   - ##### *NOTE* : change `<PATH-TO>` to your local directory path:
3. run all test playbooks with `python3 main.py`

## License

[Apache 2.0 license](LICENSE)
