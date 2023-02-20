# Runs all playbook tests automatically, as Travis would do.
# This allows for easy, quick testing locally, though you will need to
# create your own inventory file

import subprocess
rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_install.yml', '--extra-vars', 'ibmMqLicence=accept'])
if rc.returncode == 0:
    rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'setup_test.yml'])
    if rc.returncode == 0:
        rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_absent_qmgr.yml'])
        if rc.returncode == 0:
            rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_present_qmgr.yml'])
            if rc.returncode == 0:
                rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_running_qmgr.yml'])
                if rc.returncode == 0:
                    rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_misc.yml'])
                    if rc.returncode == 0:
                        rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'test_web_console.yml'])
                        if rc.returncode == 0:
                            rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
                            if rc.returncode == 0:
                                print("<---- All Tests Completed Successfully ---->")
                            else:
                                print("<---- cleanup_test.yml failed ---->")
                        else:
                            print("<---- test_web_console.yml failed ---->")
                    else:
                        print("<---- test_misc.yml failed ---->")
                else:
                    print("<---- test_running_qmgr.yml failed ---->")
            else:
                print("<---- test_present_qmgr.yml failed ---->")
        else:
            print("<---- test_absent_qmgr.yml failed ---->")
    else:
        print("<---- setup_test.yml failed ---->")
else:
    print("<---- test_install.yml failed ---->")