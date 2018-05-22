# -*- coding:utf-8 -*-
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from celery import Celery
from config import config

db = SQLAlchemy()
compress = Compress()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    handler = logging.handlers.RotatingFileHandler(app.config['LOG_PATH'], mode='a', maxBytes=10485760,
                                                   backupCount=5, encoding='utf-8')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    db.init_app(app)
    compress.init_app(app)
    return app


def register_blue(app):
    from app.main import main
    from app.api import api
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    return app


def create_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = create_celery(create_app(os.getenv('FLASK_CONFIG') or 'default'))
from main.tasks import *
from system.tasks import *
