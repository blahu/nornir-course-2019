from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from pprint import pprint as pp
import os

def my_task(task):
    #print(dir(task))
    task.run(name="ip", task=netmiko_send_command, command_string="show ip int brief", use_textfsm=True)

nr=InitNornir(config_file="../../config.yaml")
print(f"{nr.config.core.num_workers}")

ios_filt = F(groups__contains="ios")
nr = nr.filter(ios_filt)

print(nr.inventory.hosts)

nr.inventory.hosts["cisco3"].password = 'bogus'
agg_results=nr.run(task=my_task)
print_result(agg_results)

print(f"Failed hosts from results {agg_results.failed_hosts}")
print(f"Failed hosts from data {nr.data.failed_hosts}")

if nr.data.failed_hosts:
    try:
        # Remove "cisco3" from the Nornir connection table
        nr.inventory.hosts["cisco3"].close_connections()
    except ValueError:
        pass
    nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]

nr.data.reset_failed_hosts()

agg_results=nr.run(task=my_task)
print_result(agg_results)

print(f"Failed hosts from results {agg_results.failed_hosts}")
print(f"Failed hosts from data {nr.data.failed_hosts}")

