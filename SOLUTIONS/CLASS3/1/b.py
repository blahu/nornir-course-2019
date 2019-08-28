from nornir import InitNornir
from pprint import pprint
nr=InitNornir()

for host in nr.inventory.hosts.keys():
    print(host)
    pprint(nr.inventory.hosts[host].items())
