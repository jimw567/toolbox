#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import subprocess
import json
import sys


new_ip_json = sys.argv[1]

command = 'gadmin config dump'
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
p_out = p.stdout.read().decode('utf-8')
p_returncode = p.wait()
if p_returncode != 0:
    print(p_out)

config_dict = json.loads(p_out)
print('INFO: Current cluster node IP configuration:')
for h in config_dict['System']['HostList']:
    print('ID:', h['ID'], 'Hostname:', h['Hostname'])

with open(new_ip_json, 'r') as fh:
    new_ip_dict = json.load(fh)

print('INFO: New cluster node IP configuration:')
for k in new_ip_dict.keys():
    print('ID:', k, 'Hostname:', new_ip_dict[k])

# update the HostList
host_cnt = len(config_dict['System']['HostList'])
for i in range(host_cnt):
    id = config_dict['System']['HostList'][i]['ID']
    if new_ip_dict.get(id):
        # this node needs to be updated
        config_dict['System']['HostList'][i]['Hostname'] = new_ip_dict[id]

config_str = json.dumps(config_dict['System']['HostList'])
command = "gadmin config set System.HostList '" + config_str + "'"
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
p_out = p.stdout.read().decode('utf-8')
p_returncode = p.wait()
if p_returncode != 0:
    print(p_out)
    exit(1)

print('INFO: ' + command + ' completed successfully.')
print('    ', p_out)

command = 'gadmin config apply -y'
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
p_out = p.stdout.read().decode('utf-8')
p_returncode = p.wait()
if p_returncode != 0:
    print(p_out)
    exit(2)

print('INFO: ' + command + ' completed successfully.')
print('    ', p_out)

command = 'gadmin stop all && admin start infra && gadmin start all'
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
p_out = p.stdout.read().decode('utf-8')
p_returncode = p.wait()
if p_returncode != 0:
    print(p_out)
    exit(3)

print('INFO: ' + command + ' completed successfully.')
print('    ', p_out)

print('INFO: Cluster node IP configuration updated to:')
for h in config_dict['System']['HostList']:
    print('ID:', h['ID'], 'Hostname:', h['Hostname'])

print('******************************************')
print('INFO: Rebooting all nodes may be required')
print('******************************************')

