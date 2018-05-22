# -*- coding:utf-8 -*-
import time
from flask import request, jsonify
from app.main.models import IOPS, Container, IOPSEveryIntervalHour, DiskInfo
from . import api


@api.route('/iops/array/disk/<int:disk_id>')
def disk_iops_api(disk_id):
    disk = DiskInfo.query.filter_by(id=disk_id).first()

    if not disk:
        return jsonify({'error': 'specified disk not exist'}), 404
    timestamp = long(time.time())
    recent = request.args.get('recent', 1, type=int)
    first = request.args.get('start', None, type=long)
    second = request.args.get('end', timestamp, type=long)

    if not first:
        first = timestamp - recent * 3600
        second = timestamp

    if (second - first) > 24 * 3600:
        iops_table = IOPSEveryIntervalHour
    else:
        iops_table = IOPS.model(disk.container.array.name.replace('-', '_'))

    ios = iops_table.query.filter(iops_table.disk_id == disk_id).filter(iops_table.time.between(first, second)).all()

    iops = []
    for io in ios:
        if iops[-1]['timestamp'] != io.time or not iops[-1]:
            iops.append({
                'timestamp': io.time,
                'iops': {io.disk_name: io.io}
            })
        else:
            iops[-1]['iops'][io.disk_name] = io.io

    return jsonify(iops), 200


@api.route('/iops/array/container/<int:container_id>', methods=['GET'])
def container_iops_api(container_id):
    container = Container.query.filter_by(id=container_id).first()
    if not container:
        return jsonify({'error': 'specified container not exist'}), 200

    timestamp = long(time.time())
    recent = request.args.get('recent', 1, type=int)
    first = request.args.get('start', None, type=long)
    second = request.args.get('end', timestamp, type=long)
    if not first:
        first = timestamp - recent * 3600
        second = timestamp

    if (second - first) > 24 * 3600:
        iops_table = IOPSEveryIntervalHour
    else:
        iops_table = IOPS.model(container.array.name.replace('-', '_'))

    iops = []
    ios = iops_table.query.filter_by(container_id=container_id).filter(iops_table.time.between(first, second)).order_by(iops_table.time.asc()).all()
    if ios:
        for io in ios:
            if not iops or iops[-1]['timestamp'] != io.time or not iops[-1]:
                iops.append({
                    'timestamp': io.time,
                    'iops': {io.disk_name: io.io}

                    })
            else:
                iops[-1]['iops'][io.disk_name] = io.io

        return jsonify(iops), 200
    return jsonify([]), 200
