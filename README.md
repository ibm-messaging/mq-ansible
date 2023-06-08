# *MQ-Ansible*

| :memo:        | Interested in contributing to this project? Please read our [IBM Contributor License Agreement](CLA.md) and our [Contributing Guide](CONTRIBUTING.md).       |
|---------------|:------------------------|

A collection for automating the installation and configuration of IBM MQ using Ansible on Ubuntu, Redhat and Windows machines. Our aim is to make MQ-Ansible extensible for other platforms and more detailed IBM MQ configuration.

This directory contains:
- ansible [`roles`](https://github.com/ibm-messaging/mq-ansible/tree/main/ansible_collections/ibm/ibmmq/roles) for the installation and configuration of IBM MQ.
- module [`queue_manager.py`](ansible_collections/ibm/ibmmq/library/queue_manager.py) to create and configure a queue manager.
- playbook [`ibmmq.yml`](ansible_collections/ibm/ibmmq/ibmmq.yml) which implements the roles and module.

For a detailed explanation and documentation on how MQ-Ansible works, click [here](https://github.com/ibm-messaging/mq-ansible/wiki).

## Requirements

- `ansible`, `passlib` and `ansible-lint` are required on your local machine to run playbooks implementing this collection.
- a target machine of any of the supported platforms:
  - Ubuntu
  - RedHat
  - Windows

 ##### *Ansible* installation ([Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

## Installation roles on Windows machines.

Detailed documentation and guide for installing MQ on Windows using our roles can be found [here](ansible_collections/ibm/ibmmq/library/WINSTALL.md).

## Playbooks and Roles for IBM MQ installation on Ubuntu target machines

The playbooks and roles in this collection carry out an installation of IBM MQ Advanced on a target machine. The roles have been implemented to set up the required users on the machine, download the software, install and configure IBM MQ, copy over a configurable `dev-config.mqsc` file ready to be run on the target machine, and setup and start the web console. Developers can change this file to customise the configuration of their queue managers. Here we use a playbook that calls other playbooks but you can run the roles in playbooks to suit your requirements.

### Example Playbooks

`ibmmq.yml` - this playbook calls the mq-install and mq-setup playbooks, host names are passed into the imported playbook variable as {{ ansible_play_batch }}

```yaml
- name: Install and setup IBM MQ
  hosts: ['servers']

- name: Run the install playbook
  import_playbook: mq-install.yml

- name: Run the setup playbook
  import_playbook: mq-setup.yml
```

`mq-install.yml` - this playbook installs IBM MQ with the SSH user specified in the inventory.
##### *Note*: The MQ *version* and app user's *UID and GID* can be specified here.
```yaml
- hosts: "{{ ansible_play_batch }}"
  serial: 1
  become: false
  environment:
    PATH: /opt/mqm/bin:{{ ansible_env.PATH }}

  roles:
    - role: setupusers
      vars:
        appUid: 909
        appGid: 909
        mqmHome: /home/mqm
        mqmProfile: .profile
    - role: downloadmq
      vars:
        version: 930
    - role: installmq-linux
```
`mq-setup.yml` - this playbook sets up IBM MQ using the 'mqm' user

```yaml
- hosts: "{{ ansible_play_hosts }}"
  serial: 1
  become: yes
  become_user: mqm
  environment:
    PATH: /opt/mqm/bin:{{ ansible_env.PATH }}

  roles:
    - getconfig
    - setupconsole
    - startconsole

  tasks:

    - name: Create a queue manager
      queue_manager:
        qmname:
        - 'QM1'
        - 'QM2'
        state: 'present'
```
### Roles

`setupusers` - creates the `mqm`, `admin`, and `app` users; the `mqm`, `mqclient` groups; and sets the MQ environment variables. User and group IDs can be specified when calling this role. 

`downloadmq` - downloads and unzips the appropriate MQ package based on the target platform to `/var/MQServer` on the target machine. The MQ version to be installed can be specified when calling this role.

`installmq-linux` - handles platform-specific installation steps, where Ubuntu machines carry out a Debian installation and RedHat machines carry out an RPM installation. Core MQ components are installed as default, however further components and languages can be be added by uncommenting packages within the `package_files` list in  `/roles/installmq-linux/tasks/main.yml`:

```yaml
- name: Find required package files
  find:
    paths: "/var/MQServer"
    use_regex: yes
    patterns: "{{ item }}"
  register: package_files
  with_items: 
    - '(?i).*runtime.*'
    - '(?i).*server.*'
    - '(?i).*java.*'
    - '(?i).*jre.*'
    - '(?i).*sdk.*'
    - '(?i).*samples.*'
    - '(?i).*man.*'
    - '(?i).*client.*'
    - '(?i).*gskit.*'
    - '(?i).*amqp.*'
    - '(?i).*ams.*'
    - '(?i).*web.*'
    - '(?i).*(-|_)es.*'
    - '(?i).*(-|_)cn.*'
    # - '(?i).*ftbase.*'
    # - '(?i).*ftlogger.*'
    # - '(?i).*fttools.*'
    # - '(?i).*ftagent.*'
    # - '(?i).*ftservice.*'
    # - '(?i).*xrservice.*'
    # - '(?i).*sfbridge.*'
    # - '(?i).*bcbridge.*'
    # - '(?i).*(-|_)de.*'
    # - '(?i).*(-|_)fr.*'
    # - '(?i).*(-|_)ja.*'
    # - '(?i).*(-|_)it.*'
    # - '(?i).*(-|_)ko.*'
    # - '(?i).*(-|_)ru.*'
    # - '(?i).*(-|_)pt.*'
    # - '(?i).*(-|_)hu.*'
    # - '(?i).*(-|_)pl.*'
    # - '(?i).*(-|_)cs.*'
    # - '(?i).*(-|_)tw.*'
```
##### *Note*: For Ubuntu, dependencies are sensitive to the order of regex-matched packages in the `with_items` attribute of the above task. 

`getconfig` - copies the dev-config.mqsc file to the target machine.

`setupconsole` - configures a target machine's environment and permissions to be able to run the MQ Web Console.

`startconsole` - starts the MQ Web Console.

## Modules for IBM MQ resources' configuration

- `queue_manager.py` - Creates, starts, deletes an IBM MQ queue manager and runs an MQSC file. See the documentation [here.](QUEUE_MANAGER.md)

# Run our sample playbook

##### *Note*: *Ansible* must be installed on the local machine ([Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

Before running the playbook and implementing our modules and roles for IBM MQ:

1. Check if you have an *ssh* key pair in order to access the target machines via SSH. Go to the `~/.ssh` directory in your machine and look for the public and private key files e.g. `id_rsa` and `id_rsa.pub`.

    ```shell
     cd ~/.ssh
    ```

2. If those two files are not in your `ssh` directory, you need to generate `id_rsa` and `id_rsa.pub` with the following command:

    ```shell
     ssh-keygen
    ```

3. Once the keys have been generated, you need to copy the public key to the target machine's user `ssh` directory.

    ```shell
     ssh-copy-id -i id_rsa.pub [USER]@[YOUR_TARGET_HOST]
    ```
    
4. To confirm the keys have been copied successfully, connect to your target machine by:

    ```shell
     ssh [USER]@[YOUR_TARGET_HOST]
    ```
    This should connect to your target machine without asking for a password.
    
5. On your local machine clone this repository. 

6. Go to the `ansible_collections/ibm/ibmmq/` directory.

    ```shell
     cd mq-ansible/ansible_collections/ibm/ibmmq/
    ```


7. Create a file `inventory.ini` inside the directory with the following content:
  
    ```ini
    
    [servers]
    YOUR_HOST_ALIAS ansible_host=YOUR_HOSTNAME ansible_ssh_user=YOUR_SSH_USER
    YOUR_HOST_ALIAS ansible_host=YOUR_HOSTNAME ansible_ssh_user=YOUR_SSH_USER

    ```
   ##### *Note*: you can specify one or more hosts
   - Change `YOUR_HOST_ALIAS` to an alias name that you wish to use e.g. `mq-host-1` , you can omit aliases if you prefer
   - Change `YOUR_HOSTNAME` to your server/hostname, e.g. `myserver-1.fyre.com`
   - Change `YOUR_SSH_USER` to your target machine's SSH user
   ##### *Note*: the user on the target machine MUST have `root` or `sudo` privileges

### ibmmq.yml

The sample playbook [`ibmmq.yml`](ansible_collections/ibm/ibmmq/ibmmq.yml) installs IBM MQ Advanced with our roles and configures a queue manager with the `queue_manager.py` module. 

1. Before running the playbook, ensure that you have added the following directory path to the ANSIBLE_LIBRARY environment variable.

    ##### *Note*: change `<PATH-TO>` to your local directory path:

    - On Mac:

       ```shell
          export ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY}:<PATH-TO>/mq-ansible/ansible_collections/ibm/ibmmq/library
       ```

    - On Windows:
    
      ```shell
          set ANSIBLE_LIBRARY=%ANSIBLE_LIBRARY%;<PATH-TO>/mq-ansible/ansible_collections/ibm/ibmmq/library
       ```

2. Run the following command to execute the tasks within the playbook:
      ```shell
       ansible-playbook ./ibmmq.yml -i inventory.ini -e 'ibmMqLicence=accept'
      ```
      - ##### *Note*: you can optionally add `-K` (uppercase) to the command, this will prompt the user to enter the sudo password for [YOUR_SSH_USER] on the target machine, you can omit if you have setup SSH keys

3. The playbook should return the result of `dspmq` with the queue manager created listed. Log into your target machine and check it manually:

    ```shell
     dspmq
    ```

# Troubleshooting

If one of the following errors appears during the run of the playbook, run the following commands according to the problem:

- `Please add this host's fingerprint to your known_hosts file to manage this host.` - Indicates that an SSH password cannot be used instead of a key. 
  
  Fix:
  ##### *Note*: change `[YOUR_HOST]` to the target machine's network address
  ```shell
  ssh-keyscan -H [YOUR_HOST] >> ~/.ssh/known_hosts
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

1. copy your `inventory.ini` file to the `tests/playbooks` directory 
    ```shell
     cp inventory.ini tests/playbooks
    ```
2. go to the `tests/playbooks` directory 
    ```shell
     cd tests/playbooks
    ```
3. export the modules to your Ansible library
    ```shell
     export ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY}:<PATH-TO>/ansible_mq/ansible_collections/ibm/ibmmq/library
    ```
   - ##### *Note*: change `<PATH-TO>` to your local directory path:
4. run all test playbooks
    ```shell
      python3 main.py
    ```

## License

[Apache 2.0 license](LICENSE)
