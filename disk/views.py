import json
import os
from django.core import serializers
from django.http import HttpResponse
from disk.models import Disk


def disk(req):
    """
    hit the database to get saved disk usage and return all disk models in json
    """
    disks = Disk.objects.all()
    return HttpResponse(serializers.serialize('json', disks), content_type='application/json')


def update_disks(req):
    """
    calculate disk usage and update the models
    """
    disks = Disk.objects.all()
    disk_list = []
    for disk in disks:
        result = os.statvfs(disk.name)
        bytes_per_block = result.f_frsize
        blocks_available = result.f_bavail
        available_terabytes = float(blocks_available) * float(bytes_per_block) / 1099511627776
        total_blocks = result.f_blocks
        capacity_terabytes = float(total_blocks) * float(bytes_per_block) / 1099511627776
        disk.capacity_terabytes = capacity_terabytes
        disk.available_terabytes = available_terabytes
        disk.save()
        disk_dict = {
            'name': disk.name,
            'available_terabytes': available_terabytes,
            'capacity_terabytes': capacity_terabytes
        }
        disk_list.append(disk_dict)
    disks_json = json.dumps(disk_list)
    return HttpResponse(disks_json, content_type='application/json')
