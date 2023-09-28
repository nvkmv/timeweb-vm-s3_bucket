import json
import os
from time import sleep

BUCKET_NAME = "example-s3-bucket"
SERVER_NAME = "s3"

os.system('terraform apply -auto-approve')
sleep(10)
os.system('terraform show -json > tfs.json')

with open('tfs.json') as f:
    data = json.load(f)

#get s3 creds

if 'values' in data:
    resources = data['values']['root_module']['resources']
    for item in resources:
        if item['name'] == BUCKET_NAME:
            access_key = item['values']['access_key']
            with open('ansible/group_vars/s3.yml', 'w') as file:
                file.write(f"access_key: {access_key}\n")

if 'values' in data:
    resources = data['values']['root_module']['resources']
    for item in resources:
        if item['name'] == BUCKET_NAME:
            secret_key = item['values']['secret_key']
            with open('ansible/group_vars/s3.yml', 'a') as file:
                file.write(f"secret_key: {secret_key}\n")

    for item in resources:
        if item['name'] == BUCKET_NAME:
            bucket_name = item['values']['full_name']
            with open('ansible/group_vars/s3.yml', 'a') as file:
                file.write(f"bucket_name: {bucket_name}")

# get ip address VM
if 'values' in data:
    resources = data['values']['root_module']['resources']
    for item in resources:
        if item['name'] == SERVER_NAME:
            ipv4 = item['values']['main_ipv4']
            with open('ansible/hosts', 'w') as file:
                file.write(
                    f"[vps]\n {ipv4} ansible_ssh_user=root ansible_user=root")

sleep(180)
os.chdir('ansible')
os.system('ansible-playbook playbook.yml')
