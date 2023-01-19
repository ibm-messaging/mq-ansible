# Contributing to MQ-Ansible 

Thank you for your interest in contributing to our open-source project, MQ-Ansible. 

To ensure that the codebase is always healthy and does not result in deployment issues when cloned and used, it is important that you pre-check your additions and updates for any potential code conflicts before uploading your changes to the GitHub Repository. 

Therefore, the following steps should be followed to submit your contributions: 

1. Clone the project and create a new branch 
2. Create and run Ansible Test Playbooks
3. Commit changes to your branch
4. Prepare a Pull Request 
5. Submit the Pull Request 


### 1. Clone the project and create a new branch 

Once you have cloned the project, create a new branch by running: 

```
git checkout <your_branch_name> 
```

You can work locally and commit to your changes to your newly created branch. This will not impact the main branch. If you are looking to add all the files you have modified in a particular directory, you can stage them all with the following command:

```
git add . 
```

If you are looking to recursively add all changes including those in subdirectories, you can type: 

```
git add -A 
```

Alternatively, you can type _git add -all_ for all new files to be staged. 

### 2. Create and run Ansible Test Playbooks

Before committing changes, ensure that they work with the main codebase. 

In the repository, navigate to “~/tests/playbooks”. You will find a group of YAML playbooks that will ensure the deployment is still successful with your proposed changes. 

For any additions you contribute with, you will also need to write “assert that” statements to confirm that your changes will not break the codebase or cause any issues. You can go through the Python files in the directory to get an idea of how these Test Playbooks should be structured.

After writing your Test Playbooks, make sure to include them in the “main.py” file to execute all of the Test Playbooks at once. It will look something like this: 

```
subprocess.run(['ansible-playbook', '--inventory', 'inventory.ini', 'playbook_name.yml']) 
```

If the playbook runs successfully and no errors are displayed, then proceed to Step #3. 

### 3. Commit changes to your branch 

Once you are ready to submit your changes, ensure that you commit them to your branch with a message. The commit message is an important aspect of your code contribution; it helps the maintainers of MQ-Ansible and other contributors to fully understand the change you have made, why you made it, and how significant it is. 

You can commit your changes by running: 

```
git commit -m "Brief description of your changes/additions"
```

Once you have committed, you can verify what Git will be committing with the git status command.  At this point you can push the changes to the current branch of the main repository: 

```
git push --set-upstream origin <your_branch_name> 
```

### 4. Prepare a Pull Request 

Next, specify a new remote upstream repository to sync with the fork. This will be the original main repository that you forked from. You can do this by running the following command: 

```
git remote add upstream https://github.com/ibm-messaging/mq-ansible.git
```

Now, commits to the main branch will be stored in a local branch called upstream/main. Switch to the local main branch of our repository: 

```
git checkout main 
```

Merge any changes that were made in the original repository’s main branch:

```
git merge upstream/main
```

### 5. Create a Pull Request 

Before creating a Pull Request, ensure you have read the [IBM Contributor License Agreement](CLA.md). By creating a PR, you certify that your contribution:
1. is licensed under Apache Licence Version 2.0, The MIT License, or any BSD License.
2. does not result in IBM MQ proprietary code being statically or dynamically linked to Ansible runtime.

Once you have carefully read and agreed to the terms mentioned in the [CLA](CLA.md), you are ready to make a pull request to the original repository.

Navigate to your forked repository and press the _New pull request_ button. Then, you should add a title and a comment to the appropriate fields and then press the _Create pull request_ button.

The maintainers of the original repository will then review your contribution and decide whether or not to accept your pull request.
 
