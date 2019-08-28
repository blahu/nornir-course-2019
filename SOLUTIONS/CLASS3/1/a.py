from nornir import InitNornir
from pprint import pprint
nr=InitNornir()
pprint(nr.inventory.hosts["arista3"])
pprint(nr.inventory.hosts["arista3"].data)
pprint(nr.inventory.hosts["arista3"].items())
