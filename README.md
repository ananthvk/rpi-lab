# rpi-lab

## Setup

Run `uv run scripts/001_after_flash.py` after the OS image is flashed onto the storage device so that cloud-init configuration files can be written. This configures the WLAN connection, and enables the SSH server, and allows your dev machine to access the server device through pubkey authentication

Ansible test command

```
ansible myhosts -m ping -i inventory.ini -u pi
```

First do the base setup
```
ansible-playbook -i inventory.ini base_setup.yaml
```

After that do the docker setup, make sure to put `ansible-vault create group_vars/all_vault.yaml` and put your docker pat token (read only)

```
$ ansible-galaxy collection install community.docker 
$ ansible-playbook -i inventory.ini docker.yaml
```

## ansible-vault contents

```
docker_pat_token: [docker_pat_token_ro]
```
