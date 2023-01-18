# `queue_manager.py` 

Module to create, start, delete a queue manager and run MQSC file.

## Parameters

- `qmname` : IBM MQ queue manager name.
- `state` : Desired state of the queue manager (`present`, `absent`, `running`).
- `description` : IBM MQ queue manager description - *optional*.
- `unit_test`: flag used for unit tests of modules.
- `mqsc_file` : Specified MQSC command file to run - *optional*.

## Return values

- `msg` : message of the performed task.
- `rc` : return code.
- `state`

## Examples for playbooks

#### Creating queue manager task

```
- name: Create queue manager
    queue_manager:
      qmname: 'queue_manager_name'
      state: present
```

#### Starting queue manager task

```
- name: Start queue manager
    queue_manager:
      qmname: 'queue_manager_name'
      state: running
```

#### Delete queue manager task

```
- name: Start queue manager
    queue_manager:
      qmname: 'queue_manager_name'
      state: absent
```

#### Run MQSC command file task

```
- name: Run MQSC command file 
    queue_manager:
      qmname: 'queue_manager_name'
      state: running
      mqsc_file: 'commfile.in'
```

## Example of unit testing of module 

Note: Exeption classes `AnsibleExitJson` and `AnsibleFailJson` should be set. See [`test_queue_manager.py`](ansible_collections/ibm/ibmmq/tests/unit/test_queue_manager.py) for reference.

```
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
