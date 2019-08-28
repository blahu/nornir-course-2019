from nornir import InitNornir
from nornir.core.filter import F
from pprint import pprint
nr=InitNornir()
nr2=nr.filter(F(role="WAN") & F(site_details__wifi_password__contains="racecar"))
pprint(nr2.inventory.hosts.keys())


