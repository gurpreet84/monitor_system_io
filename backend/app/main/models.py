# -*- coding:utf-8 -*-

from flask import url_for
from app import db


class ArrayInfo(db.Model):
    __tablename__ = 'arrays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    ip = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(64))
    enable_crawl = db.Column(db.Boolean, default=True)
    containers = db.relationship('Container', backref='array', lazy='dynamic')

    def to_json(self):
        json_array = {
            'url': url_for('api.get_array', array_id=self.id),
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'email': self.email,
            'enable_crawl': self.enable_crawl,
            'containers': url_for('api.get_containers', array_id=self.id)
        }
        return json_array

    def __repr__(self):
        return "<ArrayInfo: %r>" % self.name


class Container(db.Model):
    __tablename__ = 'containers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(40))
    array_id = db.Column(db.Integer, db.ForeignKey('arrays.id'))
    disks = db.relationship('DiskInfo', backref='container', lazy='dynamic')

    def to_json(self):
        container_json = {
            'url': url_for('api.get_container', Container_id=self.id),
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'disks': url_for('api.get_disks', Container_id=self.id),
            'array': url_for('api.get_array', array_id=self.array_id)
        }
        return container_json

    def __repr__(self):
        return "<Container: %r>" % self.name


class DiskInfo(db.Model):
    __tablename__ = 'disks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    rpm = db.Column(db.Integer)
    isInUse = db.Column(db.Boolean, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('containers.id'))

    def to_json(self):
        disk_json = {
            'id': self.id,
            'url': url_for('api.get_disk', disk_id=self.id),
            'name': self.name
            'rpm': self.rpm,
            'isInUse': self.isInUse,
            'size': self.size,
            'container': url_for('api.get_container', Container_id=self.container_id)
        }
        return disk_json

    def __repr__(self):
        return "<DiskInfo: %r>" % self.name


class IOPS(object):
    _mapper = {}

    @staticmethod
    def model(name):
        name = name.encode('utf-8')
        ModelClass = IOPS._mapper.get(name, None)
        if ModelClass is None:
            ModelClass = type(name, (db.Model,), {
                '__module__': __name__,
                '__name__': name,
                '__tablename__': 'iops_' + name,

                'id': db.Column(db.Integer, primary_key=True),
                'disk_name': db.Column(db.String(32), nullable=False),
                'time': db.Column(db.BigInteger(), nullable=False, index=True),
                'io': db.Column(db.Float(precision=4), nullable=False),
                'container_id': db.Column(db.Integer, db.ForeignKey('containers.id')),
                'disk_id': db.Column(db.Integer, db.ForeignKey('disks.id'))
            })
            IOPS._mapper[name] = ModelClass
        return ModelClass


class IOPSEveryIntervalHour(db.Model):

    __tablename__ = 'iops_interval_hour'

    id = db.Column(db.Integer, primary_key=True)
    disk_name = db.Column(db.String(32), nullable=False)
    time = db.Column(db.BigInteger(), nullable=False, index=True)
    io = db.Column(db.Float(precision=4), nullable=False)
    container_id = db.Column(db.Integer , db.ForeignKey('containers.id'))
    disk_id = db.Column(db.Integer, db.ForeignKey('disks.id'))
