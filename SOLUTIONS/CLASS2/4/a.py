from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get, napalm_cli
from pprint import pprint as pp
import re

def my_task(task):
    #print(dir(task))
    task.run(name="route", task=napalm_cli, commands=["show ip route 0.0.0.0"])
    task.run(name="arp", task=napalm_get, getters=["arp_table"])

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
        print(type(my_results.result))
        print(f"name={my_results.name} result={my_results.result}")
        print(my_results.name)
        """
        if "route" in my_results.name:
            route = my_results.result['show ip route 0.0.0.0']
            #pp(route)
            if "ios" in v.platform:
                #  '  * 10.220.88.1\n'
                for line in route.splitlines():
                    m=re.search(r"\*\s([0-9\.]+)", line)
                    if m:
                        gateway=m.group(1)
            if "eos" in v.platform:
                #  ' S      0.0.0.0/0 [1/0] via 10.220.88.1, Vlan1\n'
                for line in route.splitlines():
                    m=re.search(r"via\s([0-9\.]+),", line)
                    if m:
                        gateway=m.group(1)
    #print(gateway)
    #gateway='10.220.88.1'
    for my_results in agg_results[h]:
        if "arp" in my_results.name:
            arp_table = my_results.result["arp_table"]
            for arp in arp_table:
                if arp["ip"] == gateway:
                    print(f"Host: {h}, Gateway: {arp}")

