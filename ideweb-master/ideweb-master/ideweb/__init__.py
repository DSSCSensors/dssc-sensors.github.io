# -*- coding: utf-8 -*-
"""
ideweb
~~~~~~

Website for ChemDataExtractor.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import os
import json

from celery import Celery
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry


log = logging.getLogger(__name__)


def make_celery(app):
    """Return a configured celery app instance."""
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


def register_blueprints(app):
    """Import and register all blueprints."""
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('ideweb.default_config')

# Importing specific config settings
#app.config.from_json('/etc/config.json')

print("The apps database URI is %s" % app.config['SQLALCHEMY_DATABASE_URI'])
print("The apps broker URI is %s" % app.config['CELERY_BROKER_URL'])

# Load deployment-specific configuration from file in the instance folder
#app.config.from_pyfile('config.py', silent=True)

# Register extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
moment = Moment(app)

# Register Sentry Raven in production only
if 'SENTRY_DSN' in app.config:
    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

# Register blueprints
register_blueprints(app)


# Import view functions now app is created
from . import views, errors


@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
    """Append querystring to static file urls to force cache invalidation when they are updated."""
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too
            if blueprint and app.blueprints[blueprint].static_folder:
                static_folder = app.blueprints[blueprint].static_folder
            else:
                static_folder = app.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = int(os.stat(os.path.join(static_folder, filename)).st_mtime)
