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
                                print("<---- FATAL: cleanup_test.yml failed ---->")
                        else:
                            rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
                            print("<---- test_web_console.yml failed ---->")
                            if rc.returncode != 0:
                                print("<---- FATAL: cleanup_test.yml failed ---->")
                    else:
                        rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
                        print("<---- test_misc.yml failed ---->")
                        if rc.returncode != 0:
                            print("<---- FATAL: cleanup_test.yml failed ---->")
                else:
                    rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
                    print("<---- test_running_qmgr.yml failed ---->")
                    if rc.returncode != 0:
                        print("<---- FATAL: cleanup_test.yml failed ---->")
            else:
                rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
                print("<---- test_present_qmgr.yml failed ---->")
                if rc.returncode != 0:
                    print("<---- FATAL: cleanup_test.yml failed ---->")
        else:
            rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
            print("<---- test_absent_qmgr.yml failed ---->")
            if rc.returncode != 0:
                print("<---- FATAL: cleanup_test.yml failed ---->")
    else:
        rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
        print("<---- setup_test.yml failed ---->")
        if rc.returncode != 0:
            print("<---- FATAL: cleanup_test.yml failed ---->")
else:
    rc = subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'cleanup_test.yml'])
    print("<---- test_install.yml failed ---->")
    if rc.returncode != 0:
        print("<---- FATAL: cleanup_test.yml failed ---->")