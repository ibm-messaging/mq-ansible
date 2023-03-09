# `IBM MQ installation roles for Windows platforms` 

Our collection now also allows you to automate the download and install of IBM MQ on Windows. Different to Unix-based platforms, _Ansible_ connects to Windows hosts using Windows remote management (WinRM). Thus, as requirement, your target machine must be set up to allow the remote connection. 

## Pre-requesites

1. Set up your target machine

    Your target host must:

    - Be running either desktop Windows OS 8.1 or later, or server OSs such as Windows Server 2012 or newer. 
    - Have PowerShell 3.0 or newer and at least .NET 4.0
    - Have WinRM configured to have a listener created and activated.

    For more information on how to set up your Windows host, please refer to [Ansible documentation](https://docs.ansible.com/ansible/latest/os_guide/windows_setup.html#winrm-listener). You can also run a [_Configure Remoting for Ansible_](https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1) script to set up your Windows machine and turn on WinRM. For more details of the script, refer to the official Ansible blog [here](https://www.ansible.com/blog/connecting-to-a-windows-host). 

2. Set up your local machine

    Your local machine, where Ansible Engine will be executing the playbooks, must run Linux. You must also ensure that your local machine has ```pywinrm``` dependencies installed to use WinRM. You can do this by running ``` pip install pywinrm ```.

3. Set up Inventory file

    To indicate the Ansible Engine to use a WinRM connection, you must configure your ```ansible_connection``` host variable to ```winrm``. If you have set up your target machine with self-sigend certificates, you will also need to configure your host var to ignore certificate validtion. An example inventory file:

    ```ini
      [windows]
      YOUR_HOSTNAME

      [windows:vars]
      ansible_user=Administator
      ansible_password=YOUR_PASSWORD
      ansible_connection=winrm
      ansible_winrm_server_cert_validation=ignore
    ```

    *Note*: As installs modify Window's registry, the install can only be performed by the Administrator user. 
    - Change `YOUR_HOSTNAME` to your server/hostname, e.g. `myserver-windows.fyre.com`
    - Change `YOUR_PASSWORD` to your target machine *Administrator*'s password.

## Roles

  - ``windownloadmq``: Downloads the IBM MQ Advanced developer package to an specified directory. Default directory in our sample playbook is `C:\Users\Administrator`.
  - ``winstallmq``: Installs the package.

## Implementing the roles on your playbook

  Example based in our sample playbook `mq-winstall.yml`:

  ```yaml
  - hosts: windows

    roles:
      - role: windownloadmq
        vars:
          directory: C:\Users\Administrator
          version: 930
      - role: winstallmq
```

  To run the playbook, issue the following command on your local host:

  ```
    ansible-playbook ./mq-winstall.yml -i inventory.ini -e 'ibmMqLicense=yes'
  ```

## Troubleshooting

If one of the following errors appears during the run of the playbook, run the following commands according to the problem:

- `ERROR! A worker was found in a dead state` - macOs High Sierra and later versions may get this issue when implementing multithreading scripts. 

  Fix:
  ```shell
    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
  ```


