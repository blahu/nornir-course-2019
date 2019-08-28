from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from pprint import pprint
nr=InitNornir(config_file="../../config.yaml")
pprint(nr.inventory.hosts.items())

nr=nr.filter(F(groups__contains="eos"))
pprint(nr.inventory.hosts.items())

r=nr.run(task=netmiko_send_command, command_string="show interface status", use_textfsm=True)
print_result(r)
