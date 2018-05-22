# -*- coding:utf-8 -*-

import os
import sys
import subprocess
import urllib3; urllib3.disable_warnings()
from app import create_app, db, register_blue
from flask_script import Manager, Shell, Command
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = register_blue(app)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


class CeleryWorker(Command):
    name = 'celery'
    capture_all_args = True

    def run(self, argv):
        ret = subprocess.call(
            ['celery', 'worker', '-A', 'app.celery', '-B']+argv
        )
        sys.exit(ret)


manager.add_command('celery', CeleryWorker())


if __name__ == '__main__':
    manager.run()
