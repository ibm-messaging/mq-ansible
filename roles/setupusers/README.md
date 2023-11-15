# SetupUsers

### Parameters
Configures the relevant users required to install MQ on the target machine.

| Name | Description | Example |
| --- | --- | --- |
| app_uid | Unique user identifier for `app` | `909` |
| gid| Unique group identifier for `mqm` | `909` |
| app_gid | Unique group identifier for `mqclient` | `909` |
| mqm_home | Home path for MQ users | `/home/mqm` |
| mqm_profile | Path for MQ users' profile | `.profile` |
| mqm_shell | Default shell for platform | `/bin/bash` |
