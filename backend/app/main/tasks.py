# -*- utf-8 -*-
from __future__ import division

import time
import re

from app.main.models import IOPS, ArrayInfo, DiskInfo, Container, IOPSEveryIntervalHour
from app import db, celery
from app.util import get_disk, get_disk_iops


@celery.task(name="get_iops_interval_5m")
def get_iops():
    arrays = ArrayInfo.query.filter_by(enable_crawl=True).all()
    if arrays:
        for array in arrays:
            execute_info.delay(array.ip, 300)
    else:
        return None


@celery.task(name="get_iops_interval_1h")
def get_iops():
    arrays = ArrayInfo.query.filter_by(enable_crawl=True).all()
    if arrays:
        for array in arrays:
            execute_info.delay(array.ip, 3600)
    else:
        return None


@celery.task
def execute_info(ip, interval):
    iopses = get_disk_iops(ip, interval)
    array = ArrayInfo.query.filter_by(ip=ip).first()
    if interval > 300:
        iops_table = IOPSEveryIntervalHour
    else:
        iops_table = IOPS.model(array.name.replace('-', '_'))
    timestamps = iopses['timestamp']

    values = []
    for disk, ios in iopses['iops'].iteritems():
        splitDiskName = re.match(r'(\S+)_disk\S+', disk)
        container = Container.query.filter_by(name=splitDiskName.group(1), array_id=array.id).first()
        disk_id = DiskInfo.query.filter_by(name=disk, container_id=container.id).first().id
        for t, io in zip(timestamps, ios):
            io_instance = iops_table(disk_name=disk, time=t, io=io, disk_id=disk_id, dape_id=container.id)
            values.append(io_instance)

    db.session.add_all(values)
    db.session.commit()


@celery.task
def add_disk(id):
    array = ArrayInfo.query.filter_by(id=id).first()
    arrayinfo = get_disk(array.ip)
    for key, v in arrayinfo:
        value = []
        container = Container(name=key, array=array, description=v[0][1])
        value.append(container)
        if v[1]:
            for d, info in v[1].iteritems():
                disk = DiskInfo(name=d,
                                container=container,
                                rpm=info['rpm'],
                                isInUse=info['isInUse'],
                                size=info['size'])
                value.append(disk)
        db.session.add_all(value)
    db.session.commit()


@celery.task(name="update_disk")
def update_disk():
    arrays = db.session.query(ArrayInfo).all()
    for array in arrays:
        arrayinfo = get_disk(array.ip)
        containers = array.containers
        value = update_disk_info(arrayinfo=arrayinfo, array=array, containers=containers)
        db.session.add_all(value)

    db.session.commit()


def update_disk_info(arrayinfo, array, containers, type):
    value = []
    for key, v in arrayinfo:
        container = containers.filter_by(name=key).first()
        if container:
            container.description = v[0][1]
            if v[1]:
                for d, info in v[1].iteritems():
                    disk = container.disks.filter_by(name=d).first()
                    if disk:
                        disk.rpm = info['rpm']
                        disk.isInUse = info['isInUse']
                        disk.size = info['size']
                    else:
                        disk = DiskInfo(name=d,
                                        container=container,
                                        rpm=info['rpm'],
                                        isInUse=info['isInUse'],
                                        size=info['size'])

                    value.append(disk)

        else:
            container = Container(name=key, array=array, description=v[0][1])
            if v[1]:
                for d, info in v[1].iteritems():
                    disk = DiskInfo(name=d,
                                    container=container,
                                    rpm=info['rpm'],
                                    isInUse=info['isInUse'],
                                    size=info['size'])
                    value.append(disk)

        value.append(container)
    return value


@celery.task(name="delete_iops_periodic")
def delete_iops_periodic():
    arrays = ArrayInfo.query.all()
    timestamp = long(time.time()) - 14 * 24 * 3600
    for array in arrays:
        table_name = 'iops_' + array.name.replace('-', '_')
        sql_delete = "delete from {table} where time<'{timestamp}'".format(table=table_name, timestamp=timestamp)
        db.engine.execute(sql_delete)

    sql_delete_1h = "delete from {table} where time<'{timestamp}'".format(table=IOPSEveryIntervalHour.__tablename__, timestamp=timestamp)
    db.engine.execute(sql_delete_1h)
