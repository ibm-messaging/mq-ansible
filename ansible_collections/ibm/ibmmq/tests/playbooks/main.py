# Runs all playbook tests automatically, as Travis would do.
# This allows for easy, quick testing locally, though you will need to
# create your own inventory file

import subprocess
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_install.yml'])
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_absent_qmgr.yml'])
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_present_qmgr.yml'])
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_running_qmgr.yml'])
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_misc.yml'])
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_web_console.yml'])
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])