# *MQ-Ansible*

| :memo:        | Interested in contributing to this project? Please read our [IBM Contributor License Agreement](CLA.md) and our [Contributing Guide](CONTRIBUTING.md).       |
|---------------|:------------------------|

A collection for automating the installation and configuration of IBM MQ using Ansible on Ubuntu, Redhat, Windows and IBM AIX machines. Our aim is to make MQ-Ansible extensible for other platforms and more detailed IBM MQ configuration.

This directory contains:
- ansible [`roles`](https://github.com/ibm-messaging/mq-ansible/tree/main/roles) for the installation and configuration of IBM MQ.
- module [`queue_manager.py`](plugins/modules/queue_manager.py) to create and configure a queue manager.
- playbook [`ibmmq.yml`](playbooks/ibmmq.yml) which implements the roles and module.

For a detailed explanation and documentation on how MQ-Ansible works, click [here](https://github.com/ibm-messaging/mq-ansible/wiki).

| Section |
| :------ |
| [Requirements](https://github.com/ibm-messaging/mq-ansible#requirements) |
| [Our collection - IBM MQ installation on target machines](https://github.com/ibm-messaging/mq-ansible/README-GALAXY.md#our-collection---ibm-mq-installation-on-target-machines) |
| [Ansible Galaxy - Installation](https://github.com/ibm-messaging/mq-ansible/#ansible-galaxy---installation) |

## Requirements

- `ansible`, `passlib` and `ansible-lint` are required on your local machine to run playbooks implementing this collection.
- a target machine of any of the supported platforms:
  - Ubuntu
  - RedHat
  - Windows
  - IBM AIX

 ##### *Ansible* installation ([Installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html))

# Our collection - IBM MQ installation on target machines
The implementation of our collection can carry out an installation of IBM MQ Advanced on a target machine with Ansible roles. These roles set up the required users on the machine, download the software, install and configure IBM MQ, copy over a configurable `dev-config.mqsc` file ready to be run on the target machine, and setup and start the web console. Developers can change this file to customise the configuration of their queue managers. 

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

## Installation roles on Windows machines

Detailed documentation and guide for installing MQ on Windows using our roles can be found [here](https://github.com/ibm-messaging/mq-ansible/blob/main/docs/WINSTALL.md).

## Modules for IBM MQ resources' configuration

- `queue_manager.py` - Creates, starts, deletes an IBM MQ queue manager and runs an MQSC file. See the documentation [here.](https://github.com/ibm-messaging/mq-ansible/blob/main/docs/QUEUE_MANAGER.md)

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

  ```
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

5. Run it with

    ```
    ansible-playbook setup-playbook.yml -i ./inventory.ini -e 'ibmMqLicence=accept'
    ```

# License

[Apache 2.0 license](LICENSE) 
