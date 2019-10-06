from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result

def set_config(task, config):
    r = task.run(task=networking.napalm_configure,
        configuration=config,
        dry_run=True
    )
    from pprint import pprint as pp
    pp(r)

    result = Result(host=task.host)
    result.changed = r.changed
    result.failed = r.failed
    result.result = r.result
    return r
    return result

def main():
    nr=InitNornir(config_file="../../config.yaml")
    nr=nr.filter(name="arista4")
    print(nr.inventory.hosts.keys())
    configlet = '''
        interface Loopback123
            description Hello
    '''
    results=nr.run(task=set_config, config=configlet)
    print_result(results)

if __name__ == '__main__':
    main()
