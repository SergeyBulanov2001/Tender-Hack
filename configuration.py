class Configuration:
    # Flask
    DEBUG = True

    host = '85.143.9.63'
    port = 8000
    SERVER_NAME = "{}:{}".format(host, port)

    SUBDOMAIN_MATCH = True

    # db
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}'    # db, user, password, host, name