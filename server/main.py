from app import app

import configuration

import connection


if __name__ == '__main__':
    app.run(configuration.Configuration.host, configuration.Configuration.port)
