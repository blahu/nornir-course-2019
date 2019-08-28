from nornir import InitNornir
from pprint import pprint
nr=InitNornir()
pprint(nr.filter(name="arista1").inventory.hosts.keys())
