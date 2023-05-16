#
# Copyright 2022 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from ansible.module_utils.basic import AnsibleModule
import os.path

result = dict(
    rc=0,
    msg='',
    state='',
    output=''
)

def check_status_queue_managers():
    print("Working on this")

def state_present(module, unitTest):
    for qmName in module.params['qmname']:
        if module.params['unit_test'] is False:
            rc, stdout, stderr = module.run_command(['crtmqm', qmName])
            result['rc'] = rc

            if rc == 8:
                module.exit_json(skipped=True, state='present', msg='IBM MQ Queue Manager already exists')
            elif rc > 0:
                module.fail_json(**result)

def state_mqsc():
    print("working on this")

def state_running(module, unitTest):
    for qmName in module.params['qmname']:
        result['msg'] = 'IBM MQ queue manager \'' + str(qmName) + '\' started'
        if unitTest is False:
            rc, stdout, stderr = module.run_command(['dspmq', '-m', qmName])

            if rc == 72:
                rc, stdout, stderr = module.run_command(['crtmqm', qmname])
            
            rc, stdout, stderr = module.run_command(['strmqm', qmName])
            result['rc'] = rc

            if rc == 5:
                module.exit_json(skipped=True, state='running', msg='IBM MQ queue manager running')
            elif rc > 0:
                module.fail_json(**result)

def state_stopped(module, unitTest):
    for qmName in module.params['qmname']:
        if module.params['unit_test'] is False:
            rc, stdout, stderr = module.run_command(['endmqm', qmName])
            result['msg'] = stdout + stderr

            if rc == 16:
                result['state'] = 'absent'
                module.fail_json(**result)
            elif rc == 40:
                module.exit_json(skipped=True, state='present', msg = stdout + stderr)
            elif rc > 0:
                module.fail_json(**result)

def state_absent(module):
    result['msg'] = 'IBM MQ queue manager deleted.'
    for qmName in module.params['qmname']:
        if module.params['unit_test'] is False:
            rc, stdout, stderr = module.run_command(['dltmqm', qmName])
            result['msg'] = stdout + stderr
            result['rc'] = rc
            if rc == 5:
                module.exit_json(skipped=True, state='running', msg='IBM MQ queue manager running.')
            elif rc == 16:
                # Queue Manager does not exist
                 module.exit_json(skipped=True, state='absent', msg='AMQ8118E: IBM MQ queue manager does not exist.')
            elif rc > 0:
                module.fail_json(**result)


def main():
    qmgr_attributes = dict(
        qmname=dict(type='list', required=True, max_len=48),
        state=dict(type='str', required=True),
        description=dict(type='str', required=False),
        unit_test=dict(type='bool', default=False, required=False),
        mqsc_file=dict(type='str', required=False)
    )

    module = AnsibleModule(
        argument_spec=qmgr_attributes
    )