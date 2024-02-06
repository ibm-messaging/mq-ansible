# DownloadMQ
Retrieves and unpackages the specified MQ installation.

### Parameters

| Name | Description | Example |
| --- | --- | --- |
| version | Non-separated MQ version number to be installed | `930` |
| downloadURL| Download location for MQ installation | `https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/messaging/mqadv/` |
| local_source | Bool to specify if you want a local source (from Ansible machine) to be installed in your target machines |
| mq_local_path | Path where MQ source package is located locally |

### Installing from local source

To specify a local source, set the `local_source` and `mq_local_path` for the `downloadmq` role as follows:

  ```yaml
  - role: downloadmq
      vars:
        local_source: true
        mq_local_path: YOUR_PATH
  ```
  Where `YOUR_PATH` is the local path to the MQ source package. Example: `/Users/user1/Downloads/mqadv_dev932_ubuntu_x86-64.tar.gz`