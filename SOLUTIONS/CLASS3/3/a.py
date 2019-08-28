from nornir import InitNornir
from nornir.core.filter import F
from pprint import pprint
nr=InitNornir()
pprint(nr.filter(F(role="AGG")).inventory.hosts.keys())


