from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result


COMMANDS = { 
    'ios' : 'show version | inc uptime',
    'nxos' : 'show version | inc uptime',
    'eos' : 'show version | inc Uptime',
    'junos': 'show system uptime | match System'
}


def parse_uptime(uptime_string):

    """
srx2 junos show system uptime | match System
System booted: 2018-10-03 20:51:06 PDT (48w5d 00:13 ago)

cisco4 ios show version | inc uptime cisco4 uptime is 48 weeks, 5 days, 44 minutes
cisco3 ios show version | inc uptime cisco3 uptime is 16 weeks, 6 days, 23 hours, 10 minutes
nxos2 nxos show version | inc uptime Kernel uptime is 152 day(s), 21 hour(s), 10 minute(s), 57 second(s)

nxos1 nxos show version | inc uptime Kernel uptime is 152 day(s), 21 hour(s), 18 minute(s), 40 second(s)

arista3 eos show version | inc Uptime Uptime:                 22 weeks, 2 days, 18 hours and 14 minutes
arista1 eos show version | inc Uptime Uptime:                 22 weeks, 2 days, 18 hours and 33 minutes
arista2 eos show version | inc Uptime Uptime:                 24 weeks, 5 days, 3 hours and 5 minutes
arista4 eos show version | inc Uptime Uptime:                 22 weeks, 2 days, 18 hours and 30 minutes
    """

    weeks,days,hours,minutes,seconds = (0,0,0,0,0)
    uptime_string= uptime_string.replace(' and ', ',')
    uptime_split = uptime_string.split(',')
    for chunk in uptime_split:
        if 'week' in chunk:
            weeks=int(chunk.split()[-2])
        elif 'day' in chunk:
            days=int(chunk.split()[-2])
        elif 'hour' in chunk:
            hours=int(chunk.split()[0])
        elif 'minute' in chunk:
            minutes=int(chunk.split()[0])
        elif 'second' in chunk:
            seconds=int(chunk.split()[0])
    print(weeks)
    print(days)
    print(hours)
    print(minutes)
    print(seconds)

    total=seconds + (minutes*60) + (hours*60*60) + (days*24*60*60) + (weeks*7*24*60*60)
    return total 
    


def check_uptime(task):
    print(task.host)
    platform=task.host.platform
    command=COMMANDS[platform]
    r=task.run(task=networking.netmiko_send_command, command_string=command)
    parsed=parse_uptime(r.result.strip())
    print(f"{task.host} {parsed}")

def main():
    nr = InitNornir(config_file="../../config.yaml")
    results=nr.run(task=check_uptime, num_workers=1)
    #print_result(results)
if __name__ == '__main__':
    main()
