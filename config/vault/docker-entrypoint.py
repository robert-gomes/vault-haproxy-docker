#!/usr/bin/python

import requests
import json
import time
from requests.exceptions import HTTPError, RequestException
import os
import subprocess
import logging
import jinja2 as jinja
import shutil
import sys
import random

def start_vault(vault_url):
    vault_process = subprocess.Popen(
        ['vault', 'server', '-config', '/etc/vault/config.hcl'])
    check_vault_is_up(vault_url)
    return vault_process

def init_vault(hostname):
    base_url = "https://"+hostname+":8200"
    logging.info("Initializing vault.")
    # check if token already exists
    if os.path.exists("/tokens/token.json"):
        logging.error("token already created")
        with open("/tokens/token.json", "r") as keyfile:
            keysAndRootToken = json.load(keyfile)
            
    else:
        init_data = json.dumps({'secret_shares': 1, 'secret_threshold': 1})
        response = requests.put(base_url + "/v1/sys/init", data=init_data, verify=False)
        keysAndRootToken = response.json()
        with open("/tokens/token.json","w+") as token_file:
            json.dump(keysAndRootToken, token_file)
        
    try:
        logging.warning("init error: %s", keysAndRootToken['errors'])
        logging.warning("Skipping vault initialization...")
        return None
    except KeyError:
        logging.warning("Vault is uninitialized.")
    
    keys = keysAndRootToken['keys']
    
    rootToken = keysAndRootToken['root_token']
    token_file_content = "root_token=%s\n" % rootToken
    # unseal
    for key in keys:
        token_file_content += "unseal_token_%d=%s\n" % (keys.index(key), key)
        requests.put(base_url + "/v1/sys/unseal", json.dumps({'key': key}), verify=False)
    # wait a sec for vault to be unsealed
    time.sleep(1)
    

    return rootToken

def check_vault_is_up(base_url, timeout=300):
    for i in range(timeout):
        try:
            resp = requests.get(base_url + "/v1/sys/health", verify=False)
        except requests.exceptions.ConnectionError:
            logging.info("Waiting for vault %ds...", i)
        else:
            return
        time.sleep(1)
    logging.error("Timeout waiting for vault to start")
    exit(1)

def check_vault_health(base_url, timeout=300):
    base_url = "https://"+hostname+":8200"
    for i in range(timeout):
        resp = requests.get(base_url + "/v1/sys/health", verify=False)
        if resp.status_code in [200, 429]:
            logging.info("Vault is initialized, unsealed, and active")
            return
        logging.info("Waiting for vault %ds...", i)
        logging.info(resp.status_code)
        time.sleep(1)
    logging.error("Timeout waiting for vault to be healthy")
    exit(1)


def set_config(config_template_file, variable):
    template_loader = jinja.FileSystemLoader(searchpath="./")
    template_env = jinja.Environment(loader=template_loader)
    template = template_env.get_template(config_template_file)
    config_text = template.render(variables)
    with open("/etc/vault/config.hcl", "w") as f:
        f.write(config_text)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout,level=logging.INFO)

    vault_url = os.environ.get("VAULT_URL")
    hostname = os.environ.get("HOSTNAME")

    variables = {
        "hostname": hostname,
        "vault_url": vault_url
    }

    set_config("/tmp/vault.hcl.j2", variables)
    vault_process = start_vault(vault_url)
    root_token = init_vault(hostname)

    check_vault_health(hostname)
    vault_process.wait()