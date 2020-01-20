# -*- coding: utf-8 -*-
"""
ideweb.default_config
~~~~~~~~~~~~~~~~~~~~~

Default configuration. Should be overridden when deployed.

"""

import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
SECRET_KEY = '4ef582f317d50e0c0c36a512aa45282c9259f4c1ac634cf2'
SQLALCHEMY_DATABASE_URI = 'postgresql://ideweb:ideweb@localhost/ideweb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_BROKER_URL = 'amqp://ideweb:ideweb@localhost:5672/ideweb_vhost'
CELERY_RESULT_BACKEND = 'db+postgresql://ideweb:ideweb@localhost:5432/ideweb'
CELERYD_TASK_TIME_LIMIT = 1000

UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
OUTPUT_FOLDER = os.path.join(basedir, 'outputs')
ALLOWED_EXTENSIONS = {'png', 'gif', 'jpeg', 'tif', 'jpg', 'tiff'}

RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'full'

OPSIN_PATH = '/usr/local/bin/opsin'

BASIC_AUTH_USERNAME = 'default'
BASIC_AUTH_PASSWORD = 'default'
