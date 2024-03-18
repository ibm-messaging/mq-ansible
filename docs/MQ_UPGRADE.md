# `IBM MQ Fix Pack Maintenance` 

Our collection allows you to automate the installation of IBM MQ Fix Packs via the [mq-upgrade.yml](https://github.com/ibm-messaging/mq-ansible/blob/main/playbooks/mq-upgrade.yml) playbook for Linux systems. To ensure Fix Pack applicability and maintenance conventions, refer to documentation on [Maintaining and Migrating IBM MQ](https://www.ibm.com/docs/en/ibm-mq/9.3?topic=migrating-maintaining).

## Pre-Requisites

1. Verify base installation

    Your target machine/s must have an existing installation of IBM MQ, which can be automated by running our [Sample Playbook](https://github.com/ibm-messaging/mq-ansible#run-our-sample-playbook). Verify the current version by issuing:

    ```shell
     dspmqver
    ```

2. Acquire Fix Pack

    Acquire the applicable Fix Pack from [IBM Fix Central](https://www.ibm.com/support/fixcentral) by filtering for the current IBM MQ base installation version and platform for the target machine/s.

3. End the MQ Web Server

    Check for whether the web server is running by issuing:

    ```shell
    dspmqweb
    ```

    If web console is still running, end it by issuing:

    ```shell
    endmqweb
    ```

4. End all running queue manager objects

    Check for any running queue managers for the current installation by issuing:

    ```shell
    dspmq -o installation -o status
    ```

    If any queue managers are still running, end them by issuing:

    ```shell
    endmqm QMgrName
    ```
        
    Check for any listeners associated with a queue manager by issuing:

    ```shell
    echo "DISPLAY LSSTATUS(*) STATUS" | runmqsc QmgrName
    ```

    If any listeners are still running, stop end them by issuing:

    ```shell
    endmqlsr -m QMgrName
    ```
5. Set up inventory file

     Enter the location of your playbooks, for example:

     ```shell
     cd mq-ansible/ansible_collections/ibm/ibmmq/playbooks
     ```

    Create an `inventory.ini` file containing the hostname/s of your target machine/s:

    ```ini
    [upgrades]
    YOUR_HOSTNAME
    ```

## Roles for Fix Pack installation

  - ``applyfixpack``: Copies a Fix Pack from your local machine to the target machine/s, and carries out installation of the Fix Pack. The path to your local Fix Pack must be specified in the `mq_local_path` variable when calling the role.

## Implementing the roles on your playbook

  Example based on our sample playbook `mq-upgrade.yml`, specifying the location of the Fix Pack to be installed on the target machine/s:

  ```yaml
---
- hosts: "{{ ansible_play_batch }}"
    serial: 1
    become: true
    environment:
        PATH: /opt/mqm/bin:{{ ansible_env.PATH }}

    roles:
        - role: applyfixpack
          vars:
            mq_local_path: YOUR_PATH
```

Where `YOUR_PATH` is the local path to the MQ Fix Pack. Example: `/Users/user1/Downloads/9.3.4-IBM-MQ-UbuntuLinuxX64-FP0001.tar.gz`

  
To run the playbook, issue the following command on your local host:

```
ansible-playbook ./mq-upgrade.yml -i inventory.ini -e 'ibmMqLicence=accept'
```
    
## Troubleshooting

If one of the following errors appears during the run of the playbook, carry out the suggested fixes:

- `"ERROR: Shared resources for installation at /opt/mqm are in use` - MQ objects haven't correctly been ended before installation of the Fix Packs has started. 

    Fix: 
    
    Ensure steps 3 and 4 in the [Pre-Requisites](#pre-requisites) section are completed before re-running the playbook.

- `"The task includes an option with an undefined variable. The error was: list object has no element 0"` during deb/rpm package installation - the required package files for installation were not present in the Fix Pack you specified to install.

    Fix: 
    
    Ensure that your `mq_local_path` points to the applicable Fix Pack download for the target machine/s. For instance, Ubuntu installations require a specific download containing `UbuntuLinuxX64` in the file name as opposed to just `LinuxX64`.