# `queue_manager.py`
Module to create, start, delete a queue manager and run MQSC files.

## Parameters
- `qmname` : IBM MQ queue manager name.
- `state` : Desired state of the queue manager (`present`, `absent`, `running`).
- `description` : IBM MQ queue manager description - *optional*.
- `unit_test`: Flag used for unit tests of modules.
- `mqsc_file` : Specified MQSC command file to run - *optional*.
- `data_dir` : Data directory path for queue manager (`-md` flag) - *optional*.
- `log_dir` : Log directory path for queue manager (`-ld` flag) - *optional*.
- `log_file_size` : Log file size in kilobytes (`-lf` flag) - *optional*.
- `log_primary` : Number of primary log files (`-lp` flag) - *optional*.
- `log_secondary` : Number of secondary log files (`-ls` flag) - *optional*.

## Return values
- `msg` : Message of the performed task.
- `rc` : Return code.
- `state` : State of the queue manager after the operation.

## Examples for playbooks

#### Creating a Queue Manager task
```yaml
- name: Create queue manager
  queue_manager:
    qmname: 'queue_manager_name'
    state: present
```

#### Creating a Queue Manager with custom directory paths and log settings
```yaml
- name: Create queue manager with custom paths and log settings
  queue_manager:
    qmname: 'queue_manager_name'
    state: present
    data_dir: '/path/to/data/directory'
    log_dir: '/path/to/log/directory'
    log_file_size: 8192
    log_primary: 200
    log_secondary: 200
    description: 'My custom queue manager'
```

#### Starting a Queue Manager task
```yaml
- name: Start queue manager
  queue_manager:
    qmname: 'queue_manager_name'
    state: running
```

#### Deleting a Queue Manager task
```yaml
- name: Delete queue manager
  queue_manager:
    qmname: 'queue_manager_name'
    state: absent
```

#### Run MQSC command file task
```yaml
- name: Run MQSC command file
  queue_manager:
    qmname: 'queue_manager_name'
    state: running
    mqsc_file: 'commfile.in'
```

#### Use of ALL_QMGRS value
This may be used to refer to all queue managers currently defined to a system, e.g to start/stop both QM1 and QM2 defined in mq-setup.yml.
```yaml
- name: Start all queue managers
  queue_manager:
    qmname: 'ALL_QMGRS'
    state: running
```

## Example of unit testing of a module
Note: Exception classes `AnsibleExitJson` and `AnsibleFailJson` should be set. See [`test_queue_manager.py`](ansible_collections/ibm/ibmmq/tests/unit/test_queue_manager.py) for reference.

```python
def test_delete_qm(self):
    set_module_args({
        'qmname': 'qm1',
        'state': 'absent',
        'description': 'testing',
        'unit_test': True
    })
    with self.assertRaises(AnsibleExitJson) as result:
        queue_manager.main()
    self.assertEquals(result.exception.args[0]['state'], 'absent')
```

## Example of creating a queue manager with custom paths
```python
def test_create_qm_with_paths(self):
    set_module_args({
        'qmname': 'qm1',
        'state': 'present',
        'description': 'Queue manager with custom paths',
        'data_dir': '/var/mqm/qmgrs/qm1/data',
        'log_dir': '/var/mqm/qmgrs/qm1/logs',
        'log_file_size': 8192,
        'log_primary': 10,
        'log_secondary': 20,
        'unit_test': True
    })
    with self.assertRaises(AnsibleExitJson) as result:
        queue_manager.main()
    self.assertEquals(result.exception.args[0]['state'], 'present')
```