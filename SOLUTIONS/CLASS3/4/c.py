from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from pprint import pprint
nr=InitNornir(config_file="../../config.yaml")
nr=nr.filter(F(groups__contains="eos"))
r=nr.run(task=netmiko_send_command, command_string="show interface status", use_textfsm=True)

"""
[ { 'duplex': 'full',
    'name': '',
    'port': 'Et1',
    'speed': 'unconf',
    'status': 'connected',
    'type': 'EbraTestPhyPort',
    'vlan': '1'},
  { 'duplex': 'full',
    'name': '',
    'port': 'Et2',
    'speed': 'unconf',
    'status': 'connected',
    'type': 'EbraTestPhyPort',
    'vlan': '2'},
"""
"""
r:
{'arista1': MultiResult: [Result: "netmiko_send_command"],
 'arista2': MultiResult: [Result: "netmiko_send_command"],
 'arista3': MultiResult: [Result: "netmiko_send_command"],
 'arista4': MultiResult: [Result: "netmiko_send_command"]}
"""

a_dict={}
for host in nr.inventory.hosts.keys():
    a_dict[host]={}
    for i in r[host][0].result:
        a_dict[host][i["port"]] = { "status": i["status"], "vlan": i["vlan"]}

pprint(a_dict)
    
    
