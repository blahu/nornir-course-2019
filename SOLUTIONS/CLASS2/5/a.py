from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from pprint import pprint as pp

def my_task(task):
    #print(dir(task))
    task.run(name="ip", task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)

nr=InitNornir(config_file="../../config.yaml")
print(f"{nr.config.core.num_workers}")

ios_filt = F(groups__contains="ios")
nr = nr.filter(ios_filt)

print(nr.inventory.hosts)

agg_results=nr.run(task=my_task)

print_result(agg_results)
