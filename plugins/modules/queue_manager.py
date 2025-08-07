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
import re

result = dict(
    rc=0,
    msg='',
    state='',
    output=''
)

def check_status_queue_managers(qmname, module):
    rc, stdout, stderr = module.run_command(['dspmq', '-m', qmname])

    if stdout is not None:
        if 'Running' in stdout:
            return True
   
    return False


def build_crtmqm_command(qmname, module):
    """Build the crtmqm command with all supported flags"""
    cmd = ['crtmqm']
    
    # Add data directory if specified
    if module.params.get('data_dir'):
        cmd.extend(['-md', module.params['data_dir']])
    
    # Add log directory if specified
    if module.params.get('log_dir'):
        cmd.extend(['-ld', module.params['log_dir']])
    
    # Add log file size if specified
    if module.params.get('log_file_size'):
        cmd.extend(['-lf', str(module.params['log_file_size'])])
    
    # Add log primary files if specified
    if module.params.get('log_primary'):
        cmd.extend(['-lp', str(module.params['log_primary'])])
    
    # Add log secondary files if specified
    if module.params.get('log_secondary'):
        cmd.extend(['-ls', str(module.params['log_secondary'])])
    
    # Add queue manager description if specified
    if module.params.get('description'):
        cmd.extend(['-c', module.params['description']])
    
    # Add queue manager name at the end
    cmd.append(qmname)
    
    return cmd


def state_present(qmname, module):
    if module.params['unit_test'] is False:
        # Use the function to build the command with all parameters
        cmd = build_crtmqm_command(qmname, module)
        rc, stdout, stderr = module.run_command(cmd)
        result['rc'] = rc

        if module.params['mqsc_file'] is not None:
            result['rc'], result['msg'], result['output'] = run_mqsc_file(qmname, module)

        if rc == 0:
            result['rc'] = rc
            result['msg'] = 'IBM MQ Queue Manager Created'
            result['state'] = 'present'
        elif rc == 8:
            result['rc'] = 0
            result['msg'] = 'IBM MQ Queue Manager already exists. ' + result['msg']
            result['state'] = 'present'
        elif rc > 0:
            # Critical Error
            module.fail_json(**result)

def run_mqsc_file(qmname, module):
    is_running = check_status_queue_managers(qmname, module)
    exists = os.path.isfile(module.params['mqsc_file'])
    
    if exists is True:
        if is_running:
            rc, stdout, stderr = module.run_command(["runmqsc", qmname, "-f", module.params['mqsc_file']])
            result['rc'] = rc
            result['output'] = stdout + stderr
            if rc == 0:
                result['state'] = 'running'
                result['msg'] = 'MQSC configuration successfully applied to queue manager.'
                
        else:
            rc, stdout, stderr = module.run_command(['strmqm', qmname])
            rc, stdout, stderr = module.run_command(["runmqsc", qmname, "-f", module.params['mqsc_file']])
            result['rc'] = rc
            result['output'] = stdout + stderr
            rc, stdout, stderr = module.run_command(['endmqm', qmname])
            if rc == 0:
                result['msg'] = 'MQSC configuration successfully applied to queue manager.'
    else:
        if is_running:
            result['state'] = 'running'
        result['rc'] = 16    
        result['msg'] = 'MQSC file could not be found'
    return (result['rc'], result['msg'], result['output'])


def state_running(qmname, module):
    result['msg'] = 'IBM MQ queue manager \'' + str(qmname) + '\' started.'
    result['state'] = 'running'
    if module.params['unit_test'] is False:
        rc, stdout, stderr = module.run_command(['dspmq', '-m', qmname]) 

        if rc == 72:
            # QMGR does not exist Create then set running
            cmd = build_crtmqm_command(qmname, module)
            rc, stdout, stderr = module.run_command(cmd)
            if rc > 0:
                # Critical Error
                module.fail_json(**result)
            
        rc, stdout, stderr = module.run_command(['strmqm', qmname])
        result['rc'] = rc
        result['msg'] = stdout + stderr
            

        if rc == 5 and module.params['mqsc_file'] is None:
            result['rc'] = 0
            result['msg'] = 'IBM MQ queue manager running'
            result['state'] = 'running'
        elif rc == 5 and module.params['mqsc_file']:
            run_mqsc_file(qmname, module)
        elif rc == 0: 
            
            result['state'] = 'running'
            result['msg'] = 'IBM MQ queue manager \'' + str(qmname) + '\' running.'
            
            if module.params['mqsc_file']:
                run_mqsc_file(qmname, module)
            
        else:
            # Critical Error
            module.fail_json(**result)

def state_stopped(qmname, module):
    if module.params['unit_test'] is False:
        
        if module.params['mqsc_file'] is not None:
            result['rc'], result['msg'], result['output'] = run_mqsc_file(qmname, module)

        rc, stdout, stderr = module.run_command(['endmqm', qmname])
        result['msg'] = stdout + stderr

        if rc == 16:
            result['state'] = 'absent'
            module.fail_json(**result)
        elif rc == 40:
            result['rc'] = 0
            result['msg'] = stdout + stderr
            result['state'] = 'present'
        elif rc == 0:
            result['rc'] = rc
            result['state'] = 'stopped'
        elif rc > 0:
            # Critical Error
            module.fail_json(**result)
        else:
            result['rc'] = rc
            result['state'] = 'present'

def state_absent(qmname, module):
    # result['msg'] = 'IBM MQ queue manager deleted.'
    
    if module.params['unit_test'] is False:
        
        rc, stdout, stderr = module.run_command(['dltmqm', qmname])
        result['msg'] = stdout
        result['rc'] = rc
        result['state'] = 'absent'
        
        if rc == 0:
            result['msg'] = 'IBM MQ queue manager \'' + str(qmname) + '\' deleted.'
        elif rc == 5:
            result['rc'] = 0
            result['msg'] = 'IBM MQ queue manager running.'
            result['state'] = 'running'
        elif rc == 16:
            # Queue Manager does not exist
            result['rc'] = 0
            result['msg'] = 'AMQ8118E: IBM MQ queue manager does not exist.'
            result['state'] = 'absent'
        else:
            # Critical Error
            module.fail_json(**result)

def state_invalid(qmname, module):
    result['state'] = ''
    result['msg'] = 'Unrecognised State'
    result['rc'] = 16
    module.fail_json(**result)


def main():
    qmgr_attributes = dict(
        qmname=dict(type='list', required=True, max_len=48),
        state=dict(type='str', required=True),
        description=dict(type='str', required=False),
        unit_test=dict(type='bool', default=False, required=False),
        mqsc_file=dict(type='str', required=False),
        data_dir=dict(type='str', required=False),
        log_dir=dict(type='str', required=False),
        log_file_size=dict(type='int', required=False),
        log_primary=dict(type='int', required=False),
        log_secondary=dict(type='int', required=False)
    )

    module = AnsibleModule(
        argument_spec=qmgr_attributes
    )

    if module.params['qmname'][0] == "ALL_QMGRS":
        module.params['qmname'] = re.findall("(?<=QMNAME\()([^\)]*)", module.run_command(['dspmq'])[1])
        result['qmlists'] = re.findall("(?<=QMNAME\()([^\)]*)", module.run_command(['dspmq'])[1])

    ops = {
        "present": state_present,
        "running":  state_running,
        "stopped":  state_stopped,
        "absent":   state_absent
    }

    if module.params['unit_test'] is False:
        for qmname in module.params['qmname']:
            ops.get(module.params['state'], state_invalid)(qmname, module)
    
    module.exit_json(**result)

if __name__ == '__main__':
    main()