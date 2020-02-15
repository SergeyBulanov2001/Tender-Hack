from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from app import db

import configuration

import models

import connection


migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run(configuration.Configuration.host, configuration.Configuration.port)
