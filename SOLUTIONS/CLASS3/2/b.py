from nornir import InitNornir
from pprint import pprint
nr=InitNornir()
pprint(nr.filter(role="WAN").inventory.hosts.keys())
pprint(nr.filter(role="WAN").filter(port=22).inventory.hosts.keys())
