# -*- coding: utf-8 -*-
"""
fabfile.db
~~~~~~~~~~

Database fabric tasks.
 
"""

import datetime

from fabric.api import *


def _run_as_pg(command):
    """Run command as postgres user."""
    with cd('~postgres'):
        return sudo(command, user='postgres', pty=False)


def user_exists(name):
    """ Check if a PostgreSQL user exists."""
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename = '%(name)s';"''' % locals())
    return res == "1"


@task
def upgrade():
    """Apply migrations to database."""
    with cd(env.app_dir):
        sudo('python manage.py db upgrade')


@task
def backup():
    """"""
    sudo('mkdir -p %(backup_dir)s' % env)
    ts = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    absolute_path = '%s/patsearch-%s.dump' % (env.backup_dir, ts)
    sudo('pg_dump -Fc -d %s -U %s -h localhost > %s' % (env.database_name, env.database_user, absolute_path))
    return absolute_path
