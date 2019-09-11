from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from pprint import pprint


def file_transfer(task):
    platform=task.host.platform
    src_file_name=f"{platform}/{task.host['file_name']}"
    dst_file_name=f"mateusz_{task.host['file_name']}"
    task.run(task=networking.netmiko_file_transfer,
            source_file=src_file_name,
            dest_file=dst_file_name,
            overwrite_file=True
    )
    task.run(task=networking.netmiko_send_command, 
            command_string=f"more flash:/{dst_file_name}"
    )

def main():
    nr=InitNornir()
    eos=nr.filter(F(platform="eos"))
    results=eos.run(task=file_transfer, num_workers=10)
    print_result(results)

if __name__ == '__main__':
    main()
