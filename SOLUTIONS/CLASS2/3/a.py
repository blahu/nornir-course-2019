from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import netmiko_send_command
from pprint import pprint as pp

def my_task(task):
    #print(dir(task))
    task.run(name="route", task=netmiko_send_command, command_string="show ip route", use_textfsm=True)
    task.run(name="arp", task=netmiko_send_command, command_string="show ip arp")

nr=InitNornir(config_file="../../config.yaml")
print(f"{nr.config.core.num_workers}")

ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
nr = nr.filter(ios_filt | eos_filt)

print(nr.inventory.hosts)

agg_results=nr.run(task=my_task)

for h,v in nr.inventory.hosts.items():
    #print(h)
    gateway=str()
    #print(type(agg_results[h]))

    for my_results in agg_results[h]:
        """
        pp(my_results)
        print(type(my_results))
        print(dir(my_results))
        print(my_results.__doc__)
        print(my_results.name)
        """
        if "route" in my_results.name:
            for route in my_results.result:
                #pp(route)
                if route["network"] == "0.0.0.0":
                    if "ios" in v.platform:
                        gateway=route["nexthop_ip"]
                    if "eos" in v.platform:
                        gateway=route["next_hop"]
    #print(gateway)

    for my_results in agg_results[h]:
        if "arp" in my_results.name:
            arp = my_results.result
            for line in arp.splitlines():
                if gateway in line:
                    print(f"Host: {h}, Gateway: {line}")

