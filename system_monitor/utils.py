import os
import psutil
import datetime
import platform
import django

from django.conf import settings
from django.template.defaultfilters import filesizeformat


def get_overview():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    root_disk = psutil.disk_usage('/')
    return [
        {
            'name': 'cpu_percent',
            'value': psutil.cpu_percent(interval=1),
        },
        {
            'name': 'memory_percent',
            'value': memory.percent
        },
        {
            'name': 'swap_percent',
            'value': swap.percent
        },
        {
            'name': 'root_disk_percent',
            'value': root_disk.percent
        }
    ]

def get_static_overview():
    cpu_max = 0
    try:
        cpu_max = psutil.cpu_freq().max
    except:
        pass
    cpu = f'{cpu_max} hz x {psutil.cpu_count()} cores'
    uname = platform.uname()
    memory = psutil.virtual_memory()
    root_disk = psutil.disk_usage('/')
    return [
        {
            'name': 'Host Name', 
            'value': platform.node()
        },
        {
            'name': 'OS User Name',
            'value': f'{uname.system} - {uname.release}  - {uname.machine} - {uname.processor}'
        },
        {
            'name': 'Boot Time',
            'value': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'name': 'CPU',
            'value': cpu
        },
        {
            'name': 'Memory Total',
            'value': filesizeformat(memory.total)
        },
        {
            'name': 'Root Disk Total',
            'value': filesizeformat(root_disk.total)
        },
        {
            'name': 'Python Version', 
            'value': platform.python_version()
        },
        {
            'name': 'Django Version', 
            'value': django.get_version()
        },
    ]
