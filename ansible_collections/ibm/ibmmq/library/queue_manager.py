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

    result = dict(
        rc=0,
        msg='',
        state='',
        output=''
    )

    result['state'] = module.params['state']
    if module.params['state'] != 'absent' and module.params['mqsc_file'] is not None:
        result['msg'] = 'runmqsc command ran successfully'
        result['rc'] = 0
        for qmname in module.params['qmname']:
            if module.params['unit_test'] is False:
                rc, stdout, stderr = module.run_command(['dspmq', '-m', qmname])

                if rc == 72:
                    rc, stdout, stderr = module.run_command(['crtmqm', qmname])
                if module.params['state'] == 'running':
                    rc, stdout, stderr = module.run_command(['strmqm', qmname])
                rc, stdout, stderr = module.run_command(['dspmq', '-m', qmname])

                if stdout is not None:
                    if 'Running' in stdout:
                        exists = os.path.isfile(module.params['mqsc_file'])

                        if exists is True:
                            rc_runmqsc, stdout_runmqsc, stderr_runmqsc = module.run_command(["runmqsc", qmname, "-f", module.params['mqsc_file']])
                            result['rc'] = rc_runmqsc
                            result['output'] = stdout_runmqsc + stderr_runmqsc

                            if rc == 0:
                                result['msg'] = 'MQSC configuration successfully applied to Queue Manager'

                        else:
                            result['rc'] = 16
                            result['msg'] = 'MQSC file could not be found'

                    else:
                        result['msg'] = 'Queue Manager Needs to be running to apply MQSC configuration.'
                        result['rc'] = 8
                else:
                    result['msg'] = 'Queue Manager does not exist.'
                    result['rc'] = 8

    elif module.params['state'] == 'running':
        for qmname in module.params['qmname']:
            result['msg'] = 'IBM MQ queue manager \'' + str(qmname) + '\' started'
            if module.params['unit_test'] is False:
                rc, stdout, stderr = module.run_command(['dspmq', '-m', qmname])
                if rc == 72:
                    rc, stdout, stderr = module.run_command(['crtmqm', qmname])
                rc, stdout, stderr = module.run_command(['strmqm', qmname])
                result['rc'] = rc
                if rc == 5:
                    module.exit_json(skipped=True, state='running', msg='IBM MQ queue manager running')
                elif rc > 0:
                    module.fail_json(**result)

    elif module.params['state'] == 'present':
        result['msg'] = 'IBM MQ Queue Manager Created'
        for qmname in module.params['qmname']:
            if module.params['unit_test'] is False:
                rc, stdout, stderr = module.run_command(['crtmqm', qmname])
                result['rc'] = rc

                if rc == 8:
                    module.exit_json(skipped=True, state='present', msg='IBM MQ Queue Manager already exists')
                elif rc > 0:
                    module.fail_json(**result)

    elif module.params['state'] == 'absent':
        result['msg'] = 'IBM MQ queue manager deleted.'
        for qmname in module.params['qmname']:
            if module.params['unit_test'] is False:
                rc, stdout, stderr = module.run_command(['dltmqm', qmname])
                result['msg'] = stdout + stderr
                result['rc'] = rc
                if rc == 5:
                    module.exit_json(skipped=True, state='running', msg='IBM MQ queue manager running.')
                elif rc == 16:
                    # Queue Manager does not exist
                    module.exit_json(skipped=True, state='absent', msg='AMQ8118E: IBM MQ queue manager does not exist.')
                elif rc > 0:
                    module.fail_json(**result)

    elif module.params['state'] == 'stopped':
        result['msg'] = 'Quiesce request accepted. The queue manager will stop when all outstanding work\nis complete.\n'
        for qmname in module.params['qmname']:
            if module.params['unit_test'] is False:
                rc, stdout, stderr = module.run_command(['endmqm', qmname])
                result['msg'] = stdout + stderr
                if rc == 16:
                    result['state'] = 'absent'
                    module.fail_json(**result)
                elif rc == 40:
                    module.exit_json(skipped=True, state='present', msg=stdout + stderr)
                elif rc > 0:
                    module.fail_json(**result)
    else:
        # State Unrecognized, fail_json
        result['state'] = ''
        result['msg'] = 'Unrecognised State'
        result['rc'] = 16
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
