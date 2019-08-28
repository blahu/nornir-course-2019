from nornir import InitNornir
nr=InitNornir()
for host in nr.inventory.hosts:
    h=nr.inventory.hosts[host]
    print("host={} groups={} platform={} username={} password={} port={}".
        format(h.hostname,h.groups,h.platform,h.username,h.password,h.port))
