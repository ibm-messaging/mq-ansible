# `IBM MQ installation roles for Windows platforms` 

Our collection now also allows you to automate the download and install of IBM MQ on Windows. Different to Unix-based platforms, _Ansible_ connects to Windows hosts using Windows remote management (WinRM). Thus, as requirement, your target machine must be set up to allow the remote connection. 

## Pre-requesites

1. Set up your target machine

    Your target host must:

    - Be running either desktop Windows OS 8.1 or later, or server OSs such as Windows Server 2012 or newer. 
    - Have PowerShell 3.0 or newer and at least .NET 4.0
    - Have WinRM configured to have a listener created and activated.

    For more information on how to set up your Windows host, please refer to [Ansible documentation](https://docs.ansible.com/ansible/latest/os_guide/windows_setup.html#winrm-listener). You can also run a [_Configure Remoting for Ansible_](https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1) script to set up your Windows machine and turn on WinRM. For more details of the script, refer to the official Ansible blog [here](https://www.ansible.com/blog/connecting-to-a-windows-host). 

2. Set up your local machine

    Your local machine, where Ansible Engine will be executing the playbooks, must run Linux. You must also ensure that your local machine has ```pywinrm``` dependencies installed to use WinRM. You can do this by running ``` pip install pywinrm ```.

3. Set up Inventory file

    Your inventory file should be located within the ibmmq directory:

    ```shell
     cd mq-ansible/ansible_collections/ibm/ibmmq/
    ```

    **Option 1: Plaintext variables in inventory file**

      To indicate the Ansible Engine to use a WinRM connection, you must configure your ```ansible_connection``` host variable to ```winrm```. If you have set up your target machine with self-sigend certificates, you will also need to configure your host var to ignore certificate validtion. An example inventory file:

      ```ini
        [windows]
        YOUR_HOSTNAME

        [windows:vars]
        ansible_user=Administrator
        ansible_password=YOUR_PASSWORD
        ansible_connection=winrm
        ansible_winrm_server_cert_validation=ignore
      ```

      *Note*: As installs modify Windows' registry, the install can only be performed by the Administrator user. 

      - Change `YOUR_HOSTNAME` to your server/hostname, e.g. `myserver-windows.fyre.com`
      - Change `YOUR_PASSWORD` to your target machine *Administrator*'s password.

    **Option 2:** Encrypted variables for host in inventory file

      To avoid storing plaintext passwords, we recommend using `ansible-vault` to store the Windows host variables. Your `inventory.ini` file would only consist on:

      ```ini
        [windows]
        YOUR_HOSTNAME
      ```

      Now you can encrypt the windows variables with `ansible-vault`. In your terminal, execute the following commands:

      ```shell
      ansible-vault create groups_vars/windows.yml
      ```

      This command will prompt you to create a new vault password to decrypt the variables if you haven't set one previously. 

      ```shell
      New Vault password: 
      Confirm New Vault password: 
      ```

      It will then launch your system editor where you can paste the windows host variables below:

      ```
      ansible_user: Administrator
      ansible_password: "YOUR_PASSWORD"
      ansible_connection: winrm
      ansible_winrm_server_cert_validation: ignore
      ```
      - Change `"YOUR_PASSWORD"` to your target machine *Administrator*'s password in quotes. Example: _"ansiblepassword"_ 

      After you close your editor, the file will be saved with the encrypted content. The variables will be automatically applied for the the Windows host group when targeted on a playbook.

      More information about ansible-vault and content encryption can be found [here](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-individual-variables-with-ansible-vault).


## Roles for Windows installation

  - ``downloadmq``: For Windows, downloads the IBM MQ Advanced developer package to an specified directory. Default directory in our sample playbook is `C:\Users\Administrator`. You can also specify a local source to copy to the target directory with the variable `local_source`
  - ``installmq``: Installs the package.
  - ``setupconsole``: Sets up the web console.
  - ``startconsole``: Starts the web console.

## Implementing the roles on your playbook

  Example based in our sample playbook `mq-winstall.yml`, specifying the directory, version and download URL:

  ```yaml
  - hosts: windows

    roles:
    - role: downloadmq
      vars:
        directory: C:\Users\Administrator
        version: 930
        downloadURL: "https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/messaging/mqadv/"
    - installmq
    - setupconsole
    - startconsole

```
  To specify a local source, set the `local_source` and `mq_local_path` for the `downloadmq` role as follows:

  ```yaml
  - role: downloadmq
      vars:
        local_source: true
        mq_local_path: YOUR_PATH
  ```
  Where `YOUR_PATH` is the local path to the MQ source package. Example: `/Users/user1/Downloads/mqadv_dev932_windows.zip`
  
  To run the playbook, issue the following command on your local host:

  ```
    ansible-playbook ./mq-winstall.yml -i inventory.ini -e 'ibmMqLicence=yes'
  ```

## Troubleshooting

If one of the following errors appears during the run of the playbook, run the following commands according to the problem:

- `ERROR! A worker was found in a dead state` - macOs High Sierra and later versions may get this issue when implementing multithreading scripts. 

  Fix:
  ```shell
    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
  ```