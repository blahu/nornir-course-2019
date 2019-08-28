from nornir import InitNornir
nr=InitNornir()
from pprint import pprint as pp
pp(nr.inventory)
pp(nr.inventory.hosts)
pp(nr.inventory.hosts["localhost"])
pp(nr.inventory.hosts["localhost"].hostname)
