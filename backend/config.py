# -*- coding:utf-8 -*-

import os
from datetime import timedelta
from celery.schedules import crontab
basedir = os.path.abspath(os.path.dirname(__file__))

LOGIN_URL = '/api/login'
DISK_URL = '/api/disk'
CONTAINER_URL = '/api/container'
POOL_URL = '/api/pool'
IOPS_URL = '/api/iops'
USERNAME = 'user'
PASSWORD = 'password'

class Config(object):
    # Mail config
    DEBUG = True
    LOG_PATH = os.path.join(basedir, 'log', 'flask.log')
    SECRET_KEY = os.environ.get('SECRT_KEY') or "hard to @#DFh54ewf"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
    CELERY_CONFIG = {}
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = "UTC"
    CELERYBEAT_SCHEDULE = {
        'every-5-seconds': {
            'task': 'get_cpu',
            'schedule': timedelta(seconds=5)
        },
        'every-30-minutes': {
            'task': 'get_iops_interval_5m',
            'schedule': timedelta(minutes=30)
        },
        'every-1-hour': {
            'task': 'get_iops_interval_1h',
            'schedule': crontab(hour='*', minute=5)
        },
        'every-sunday-midnight': {
            'task': 'update_disk',
            'schedule': crontab(hour=7, minute=0, day_of_week=0)
        },
        'delete-systeminfo-every-midnight': {
            'task': 'delete_system_recoder',
            'schedule': crontab(hour=0, minute=0)
        },
        'delete-iops-every-midnight': {
            'task': 'delete_iops_periodic',
            'schedule': crontab(hour=0, minute=0)
        }
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:Password123!@localhost/monitor_iops'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class Testingconfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql://root:Password123!@localhost/sqlstu'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': Testingconfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
