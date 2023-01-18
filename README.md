# *MQ-Ansible*

| :memo:        | Interested in contributing to this project? [Click here](contribution.md) to read our contributors' guide.       |
|---------------|:------------------------|

A collection for automating the installation and configuration of IBM MQ using Ansible on Ubuntu 18.04 machines. Our aim is to make MQ-Ansible extensible for further and more detailed IBM MQ configuration.

This directory contains:
- ansible [`roles`](https://github.ibm.com/James-Page/ansible_mq/tree/main/ansible_collections/ibm/ibmmq/roles) for the installation and configuration of IBM MQ.
- module [`queue_manager.py`](ansible_collections/ibm/ibmmq/library/queue_manager.py) to create and configure a queue manager.
- playbook [`ibmmq.yml`](https://github.ibm.com/James-Page/ansible_mq/blob/d00a7e8db925d2907c54bac16a573a1e33470187/ansible_collections/ibm/ibmmq/ibmmq.yml) which implements the roles and module.

For a detailed explanation and documentation on how MQ-Ansible works, read `link/to/github/pages`

## Requirements

- `ansible` and `ansible-lint` is required on your local machine to run playbooks implementing this collection.
- An Ubuntu 18.04 target machine is required to run MQ.

## Roles for IBM MQ installation

The roles in this collection carry out an installation of IBM MQ Advanced on an Ubuntu 18.04 target machine with ansible roles as yaml files. The roles have been implemented to set up the required users on the machine, download the software, install and configure IBM MQ, and copy over a configurable `dev-config.mqsc` file ready to be run on the target machine. Developers can change this file to allow better configuration of their queue managers.


### Example

```yaml
- hosts: [YOUR_TARGET_MACHINES]
  become: true
  environment:
    PATH: /opt/mqm/bin:{{ ansible_env.PATH }}

  roles: 
    - setupusers
    - downloadmq
    - installmq
    - getconfig
```

## Modules for IBM MQ resources' configuration

- `queue_manager.py`- Creates, starts, deletes a IBM MQ queue manager and runs MQSC file. See documentation [here.](QUEUE_MANAGER.md)

# Run our sample playbook

### Setup (inventory.ini)

##### Note: *Ansible* must be installed on the local machine. ([Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

Before running the playbook implementing our modules and roles for IBM MQ:

1. Check if you have an *ssh* key pair in order to access the target machines via ansible. Go to the `~/.ssh` directory in your machine and look for the `id_rsa` and `id_rsa.pub` files.

    ```shell
    $ cd ~/.ssh
    ```

2. If those two files are not in your `ssh` directory, you need to generate `id_rsa` and `id_rsa.pub` with the following command:

    ```shell
    $ ssh-keygen
    ```

3. Once the keys have been generated, these need to be copied to your target machine's `ssh` directory.

    ```shell
    $ ssh-copy-id -i id_rsa.pub root@[YOUR_TARGET_MACHINE_IP]
    ```
    
4. To confirm the keys have been copied succesfully, connect to your target machine by:

    ```shell
    $ ssh root@[YOUR_TARGET_MACHINE_IP]
    ```
    This should connect to your target machine without asking for a password.
    
5. Go to the `ansible_collections/ibm/ibmmq/` directory.

    ```shell
    $ cd ..
    $ cd ansible_collections/ibm/ibmmq/
    ```


6. Create a file `inventory.ini` inside the directory with the following content:
  
    ```ini
    [localhost\]
    [YOUR_LOCAL_HOST]

    [YOUR_TARGET_MACHINES]
    [YOUR_MACHINE_IP] ansible_ssh_user=[YOUR_USER]
    ```

   - Change `YOUR_TARGET_MACHINES` to your machines group name, for example `fyre`.
   - Change `YOUR_MACHINE_IP` to your target machine's public IP
   - Change `YOUR_USER` to your target machine's user.

### ibmmq.yml

The sample playbook [`ibmmq.yml`](https://github.ibm.com/James-Page/ansible_mq/blob/d00a7e8db925d2907c54bac16a573a1e33470187/ansible_collections/ibm/ibmmq/ibmmq.yml) installs IBM MQ Advanced with our roles and configures a queue manager with the `queue_manager.py` module.

1. Before running the playbook, ensure that you have added the directory path to the PATH environment variable.

    ##### *NOTE* : change `<PATH-TO>` to your local directory path:

    - On Mac:

          ```shell
          $ export ANSIBLE_LIBRARY=<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
          ```

    - On Windows: 

          ```shell
          $ set ANSIBLE_LIBRARY=<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
          ```

2. Make sure you update the hosts in `ibmmq.yml` name to `YOUR_TARGET_MACHINES` group from your inventory file. Our playbook has as default `fyre`.

3. Run the following command to execute the tasks within the playbook:
      ```shell
      $ sudo ansible-playbook ./ibmmq.yml -i inventory.ini
      ```
      - ##### *NOTE* : `-K` will prompt the user to enter the sudo password for [YOUR_USER] on the target machine.

4. The playbook should return the result of `dspmq` with the queue manager created listed. Log into your target machine and check it manually:

    ```shell
    $ dspmq
    ```

# Troubleshooting

If one of the following errors appear during the run of the playbook, run the following commands according to the problem:

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

These playbooks test the functionality and performance of the queue_manager module in ansible plays.

To run the test playbooks first:

1. make sure you are in the right directory 
    ```shell
    $ cd tests/playbooks
    ```
2. export the modules to your ansible library
    ```shell
    $ export ANSIBLE_LIBRARY=<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
    ```
   - ##### *NOTE* : change `<PATH-TO>` to your local directory path:
3. run all test playbooks with `main.py`

## License

[Apache 2.0 license](https://github.ibm.com/James-Page/ansible_mq/blob/more_readme_updates/LICENSE)
