# -*- coding:utf-8 -*-
from flask import request, jsonify
from sqlalchemy import or_
from . import api
from app.main.models import ArrayInfo, IOPS, DAPE, DiskInfo
from app.main.tasks import add_disk
from app import db


@api.route('/array/add', methods=['POST'])
def add_array():
    request_array = request.json
    arr = ArrayInfo.query.filter(or_(ArrayInfo.name == request_array['name'], ArrayInfo.ip == request_array['ip'])).first()
    if arr:
        return jsonify({'error': "Array has been exist", 'ok': False})

    name = request_array['name']
    ip = request_array['ip']
    email = request_array['email']
    array = ArrayInfo(name=name, ip=ip, email=email)
    db.session.add(array)
    db.session.commit()

    IOPS.model(name.replace('-', '_'))
    db.create_all()
    add_disk.delay(array.id)

    return jsonify(array.to_json())


@api.route('/array')
def get_arrays():
    arrays = ArrayInfo.query.all()
    data = []
    for array in arrays:
        data.append(array.to_json())
    return jsonify(data)


@api.route('/array/<int:array_id>')
def get_array(array_id):
    array = ArrayInfo.query.filter_by(id=array_id).first()
    if not array:
        return jsonify({'error': 'Specified array not found'})
    return jsonify(array.to_json())


@api.route('/array/<int:array_id>/container')
def get_containers(array_id):
    containers = Container.query.filter_by(array_id=array_id).all()
    if not containers:
        return jsonify({'error': 'No containerfound'})
    data = []
    for container in containers:
        data.append(container.to_json())
    return jsonify(data)


@api.route('/array/container/<int:container_id>')
def get_container(container_id):
    container = Container.query.filter_by(id=container_id).first()
    if not container:
        return jsonify({'error': 'Specified container not found'})
    return jsonify(container.to_json())


@api.route('/array/container/<int:container_id>/disk')
def get_disks(container_id):
    disks = DiskInfo.query.filter_by(container_id=container_id).all()
    if not disks:
        return jsonify({'error': 'Disk not found'})
    data = []
    for disk in disks:
        data.append(disk.to_json())

    return jsonify(data)


@api.route('/array/dape/disk/<int:disk_id>')
def get_disk(disk_id):
    disk = DiskInfo.query.filter_by(id=disk_id).all()
    if not disk:
        return jsonify({'error': 'Specified disk not found'})

    return jsonify(disk.to_json())


@api.route("/array/<int:array_id>/crawl", methods=['POST'])
def enable_disable_crawl(array_id):
    from .. import db
    array_json = request.json
    array = db.session.query(ArrayInfo).filter_by(id=array_id).first()
    crawl = array_json['crawl']
    if array:
        array.enable_crawl = crawl
        db.session.add(array)
        db.session.commit()
        return jsonify(collected=array.enable_crawl), 200
    else:
        return jsonify(error="Not found this array"), 404