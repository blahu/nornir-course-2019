from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.core.filter import F
from nornir.plugins.functions.text import print_title, print_result
from pprint import pprint


def file_transfer(task):
    platform=task.host.platform
    file_name=f"{platform}/{task.host['file_name']}"
    task.run(task=networking.netmiko_file_transfer,
            source_file=file_name,
            dest_file=f"mateusz_{task.host['file_name']}",
            overwrite_file=True
    )

def main():
    nr=InitNornir()
    eos=nr.filter(F(platform="eos"))
    results=eos.run(task=file_transfer, num_workers=10)
    print_result(results)

if __name__ == '__main__':
    main()
