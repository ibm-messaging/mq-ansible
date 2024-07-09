# *MQ-Ansible*

## Issue Support

The code in this repository is provided and maintained on a community basis, and is not covered by any IBM commercial support agreement or warranty.

For enhancements, issues and fixes you are welcome raise an issue against this repository so that it may be considered. Alternatively, you may contribute updates as per the CLA outlined below.

| :memo:        | Interested in contributing to this project? Please read our [IBM Contributor License Agreement](CLA.md) and our [Contributing Guide](CONTRIBUTING.md).       |
|---------------|:------------------------|


## What is MQ-Ansible?

A collection for automating the installation and configuration of IBM MQ using Ansible on Ubuntu, Redhat, Windows and IBM AIX machines. Our aim is to make MQ-Ansible extensible for other platforms and more detailed IBM MQ configuration.

This directory contains:
- ansible [`roles`](https://github.com/ibm-messaging/mq-ansible/tree/main/roles) for the installation and configuration of IBM MQ.
- module [`queue_manager.py`](plugins/modules/queue_manager.py) to create and configure a queue manager.
- playbook [`ibmmq.yml`](playbooks/ibmmq.yml) which implements the roles and module.

For a detailed explanation and documentation on how MQ-Ansible works, click [here](https://github.com/ibm-messaging/mq-ansible/wiki).

| Section |
| :------ |
| [Requirements](https://github.com/ibm-messaging/mq-ansible#requirements) |
| [Playbooks and Roles for IBM MQ installation](https://github.com/ibm-messaging/mq-ansible#playbooks-and-roles-for-ibm-mq-installation-on-ubuntu-target-machines) |
| [Run our sample playbook](https://github.com/ibm-messaging/mq-ansible#run-our-sample-playbook) |
| [Troubleshooting](https://github.com/ibm-messaging/mq-ansible/tree/aix-support#troubleshooting) |
| [Testing Framework](https://github.com/ibm-messaging/mq-ansible/#testing-framework) |
| [Ansible Galaxy - Installation](https://github.com/ibm-messaging/mq-ansible/#ansible-galaxy---installation) |

## Requirements

- `ansible`, `passlib` and `ansible-lint` are required on your local machine to run playbooks implementing this collection.
- a target machine of any of the supported platforms:
  - Ubuntu
  - RedHat
  - Windows
  - IBM AIX

 ##### *Ansible* installation ([Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

# Playbooks and Roles for IBM MQ installation on Ubuntu target machines
The playbooks and roles in this collection carry out an installation of IBM MQ Advanced on a target machine. The roles have been implemented to set up the required users on the machine, download the software, install and configure IBM MQ, copy over a configurable `dev-config.mqsc` file ready to be run on the target machine, and setup and start the web console. Developers can change this file to customise the configuration of their queue managers. Here we use a playbook that calls other playbooks but you can run the roles in playbooks to suit your requirements.

## Example Playbooks

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
        app_uid: 909
        app_gid: 909
        mqm_home: /home/mqm
        mqm_profile: .profile
    - role: downloadmq
      vars:
        version: 930
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

`mq-upgrade.yml` - this playbook installs an applicable fix pack to an existing MQ installation

```yaml
- hosts: "{{ ansible_play_batch }}"
  serial: 1
  become: true
  environment:
    PATH: /opt/mqm/bin:{{ ansible_env.PATH }}

  roles:
    - role: applyfixpack
      vars:
        mq_local_path: ~/tmp/
```
## Roles

- `setupusers` - creates the `mqm`, `admin`, and `app` users; the `mqm`, `mqclient` groups; and sets the MQ environment variables. User and group IDs can be specified when calling this role. 

- `downloadmq` - downloads and unzips the appropriate MQ package based on the target platform to `/var/MQServer` on the target machine. The MQ version to be installed can be specified when calling this role. 
    You can also specify a local source for the MQ source packages to be copied over to target machine. Example:

    ```yaml
    - role: downloadmq
        vars:
          local_source: true
          mq_local_path: YOUR_PATH
    ```
    Where `YOUR_PATH` is the local path to the MQ source package. Example: `/Users/user1/Downloads/mqadv_dev932_ubuntu_x86-64.tar.gz`

- `installmq` - handles platform-specific installation steps, where Ubuntu machines carry out a Debian installation and RedHat machines carry out an RPM installation. Core MQ components are installed as default, however further components and languages can be be added by uncommenting packages within the `package_files` list in  `/roles/installmq/tasks/main.yml`:

##### *Note*: For Ubuntu, dependencies are sensitive to the order of regex-matched packages in the `with_items` attribute of the above task. 

- `getconfig` - copies the dev-config.mqsc file to the target machine. You can also specify a local sourced MQSC file with the var `mqsc_local`.

- `setupconsole` - configures a target machine's environment and permissions to be able to run the MQ Web Console.

- `startconsole` - starts the MQ Web Console.

`applyfixpack` - installs a locally available fix pack to an existing MQ installation. The selected fix pack must be applicable to the MQ version already existing on the target machine.

## Modules for IBM MQ resources' configuration

- `queue_manager.py` - Creates, starts, deletes an IBM MQ queue manager and runs an MQSC file. See the documentation [here.](docs/QUEUE_MANAGER.md)

## Installation roles on Windows machines

Detailed documentation and guide for installing MQ on Windows using our roles can be found [here](docs/WINSTALL.md).

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

6. Go to the `playbooks` directory.

    ```shell
     cd playbooks
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

The sample playbook [`ibmmq.yml`](playbooks/ibmmq.yml) installs IBM MQ Advanced with our roles and configures a queue manager with the `queue_manager.py` module. 

1. Before running the playbook, ensure that you have added the following directory path to the ANSIBLE_LIBRARY environment variable.

    ##### *Note*: change `<PATH-TO>` to your local directory path:

    - On Mac:

    ```shell
      export ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY}:<PATH-TO>/mq-ansible/plugins/modules
    ```

    - On Windows:
    
    ```shell
      set ANSIBLE_LIBRARY=%ANSIBLE_LIBRARY%;<PATH-TO>/mq-ansible/plugins/modules
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


# Testing Framework

### Testing module's functionality with playbooks

These playbooks test the functionality and performance of our roles and the queue_manager module in Ansible plays. 

To run the test playbooks first:

1. Try the installation with our sample playbook. You should run `ibmmq.yml` prior.

2. copy your `inventory.ini` file to the `tests/playbooks` directory 

  ```shell
    cp inventory.ini tests/playbooks
  ```

3. go to the `tests/playbooks` directory 

  ```shell
    cd tests/playbooks
  ```

4. export the modules to your Ansible library

  ```shell
    export ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY}:<PATH-TO>/mq-ansible/plugins/modules
  ```

   - ##### *Note*: change `<PATH-TO>` to your local directory path:
5. run all test playbooks

  ```shell
    ansible-playbook --inventory 'inventory.ini' main_test.yml
  ```

6. if any of the tests fail, run:

   ```shell
      ansible-playbook --inventory 'inventory.ini' cleanup_test.yml
    ```

# Ansible Galaxy - Installation

1. First, make sure that you have the minimun required version of ansible core with

    ```
    ansible --version
    ```

2. Install the latest version from our github repo with

    ```
    ansible-galaxy collection install git+https://github.com/ibm-messaging/mq-ansible.git,main
    ```

    or the latest version in ansible galaxy with:

    ```
    ansible-galaxy collection install ibm_messaging.ibmmq      
    ```

3. In your desired working directory, make sure to create your ansible inventory `inventory.ini` with the proper target hosts, as you'll refer to them while running the playbook:

    ```
    [mqservers]
    my.mqserver-001.dev
    my.mqserver-002.dev
    ```
 
4. Create now a playbook file `setup-playbook.yml` with the following content to try our roles and modules:

```shell
  ---
    - name: prepares MQ server
      hosts: mqservers
      become: true
      environment:
        PATH: /opt/mqm/bin:{{ ansible_env.PATH }}
      collections:
        - ibm_messaging.ibmmq

      tasks:
        - name: Import downloadmq role
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.downloadmq

        - name: Import setupusers role
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.setupusers

        - name: Import installmq role
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.installmq

        - name: Import setupenvironment role
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.setupenvironment

        - name: Get MQSC file 
          become: true
          become_user: mqm
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.getconfig
          vars: 
            mqsc_local: ../../../playbooks/files/dev-config.mqsc
        
        - name: Set up web console
          become: true
          become_user: mqm
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.setupconsole

        - name: Start web console 
          become: true
          become_user: mqm
          ansible.builtin.import_role:
            name: ibm_messaging.ibmmq.startconsole

        - name: Create a queue manager
          become_user: mqm
          tags: ["queue"]
          ibm_messaging.ibmmq.queue_manager:
            qmname: queue_manager_12
            state: present

        - name: Use our MQSC File
          become: true
          become_user: mqm
          ibm_messaging.ibmmq.queue_manager:
            qmname: queue_manager_12
            state: running
            mqsc_file: /var/mqm/dev-config.mqsc
            
```

5. run it with

    ```
    ansible-playbook setup-playbook.yml -i ./inventory.ini -e 'ibmMqLicence=accept'
    ```

# License

[Apache 2.0 license](LICENSE) 
