import json
import unittest

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from ansible_collections.ibm.ibmmq.library import queue_manager

#   Ideal final solution: We'd like to import this way but neither these nor "units.compat"
# can find the ansible test directory. Right now, just use the code below
#
# We might not actually need all these modules but if we need them, setting up the
# environment properly may require the env-setup.sh file.
# from ansible.test.units.compat import unittest
# from ansible.test.units.compat.mock import patch
from unittest.mock import patch


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class TestQueueManager(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json,
                                                 )
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            queue_manager.main()

    def test_module_fail_when_name_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({
                'state': 'test'
            })
            queue_manager.main()

    def test_module_fail_when_state_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({
                'qmname': 'qm1'
            })
            queue_manager.main()

    def test_create_qm(self):
        set_module_args({
            'qmname': 'qm1',
            'state': 'present',
            'description': 'testing',
            'unit_test': True
        })
        with self.assertRaises(AnsibleExitJson) as result:
            queue_manager.main()
        self.assertEquals(result.exception.args[0]['state'], 'present')

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
        self.assertEquals(result.exception.args[0]['msg'], 'IBM MQ queue manager deleted.')

    def test_start_qmgr(self):
        set_module_args({
            'qmname': 'qm1',
            'state': 'running',
            'description': 'testing',
            'unit_test': True
        })
        with self.assertRaises(AnsibleExitJson) as result:
            queue_manager.main()
        self.assertEquals(result.exception.args[0]['state'], 'running')
        self.assertEquals(result.exception.args[0]['msg'], 'IBM MQ queue manager \'qm1\' started')
        self.assertEquals(result.exception.args[0]['rc'], 0)

    def test_runmqsc_on_qmgr(self):
        set_module_args({
            'qmname': 'qm1',
            'state': 'present',
            'description': 'testing',
            'mqsc_file': 'testing_file',
            'unit_test': True
        })
        with self.assertRaises(AnsibleExitJson) as result:
            queue_manager.main()
        self.assertEquals(result.exception.args[0]['state'], 'present')
        self.assertEquals(result.exception.args[0]['msg'], 'runmqsc command ran successfully')
        self.assertEquals(result.exception.args[0]['rc'], 0)
