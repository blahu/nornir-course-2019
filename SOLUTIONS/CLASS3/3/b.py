from nornir import InitNornir
from nornir.core.filter import F
from pprint import pprint
nr=InitNornir()
sea_and_sfo=nr.filter(F(groups__contains="sea") | F(groups__contains="sfo"))
pprint(sea_and_sfo.inventory.hosts.keys())


