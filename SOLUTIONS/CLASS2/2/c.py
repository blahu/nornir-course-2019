from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from pprint import pprint as pp
nr=InitNornir(config_file="config.yaml")
print(f"{nr.config.core.num_workers}")
filt = F(groups__contains="ios")
nr = nr.filter(filt)
print(nr.inventory.hosts)

my_results=nr.run(task=netmiko_send_command, command_string="show run | inc hostname")
print(type(my_results))
print("keys:")
pp(my_results.keys())
print("items:")
pp(my_results.items())
print("values:")
pp(my_results.values())

host_results=my_results["cisco3"]
print(type(host_results))
print(dir(host_results))
print(host_results.__doc__)
for v in host_results:
    pp(v)
