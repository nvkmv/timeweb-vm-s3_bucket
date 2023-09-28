import json
import os
from time import sleep

delay = 10

os.system('terraform apply -auto-approve')
sleep(delay)
os.system('terraform show -json > tfs.json')

with open('tfs.json') as f:
    data = json.load(f)

ADDRESS = "twc_s3_bucket.example-s3-bucket"

if 'values' in data:
    resources = data['values']['root_module']['resources']
    for item in resources:
        if item['address'] == ADDRESS:
            access_key = item['values']['access_key']
            with open('ansible/group_vars/s3.yml', 'w') as file:
                file.write(f"access_key: {access_key}\n")

if 'values' in data:
    resources = data['values']['root_module']['resources']
    for item in resources:
        if item['address'] == ADDRESS:
            secret_key = item['values']['secret_key']
            with open('ansible/group_vars/s3.yml', 'a') as file:
                file.write(f"secret_key: {secret_key}\n")

    for item in resources:
        if item['address'] == ADDRESS:
            bucket_name = item['values']['full_name']
            with open('ansible/group_vars/s3.yml', 'a') as file:
                file.write(f"bucket_name: {bucket_name}")

IP_ADDRESS = "twc_server.s3"

if 'values' in data:
    resources = data['values']['root_module']['resources']
    for item in resources:
        if item['address'] == IP_ADDRESS:
            ipv4 = item['values']['main_ipv4']
            with open('ansible/hosts', 'w') as file:
                file.write(
                    f"[vps]\n {ipv4} ansible_ssh_user=root ansible_user=root")
