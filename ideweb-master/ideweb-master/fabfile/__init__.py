# -*- coding: utf-8 -*-
"""
ideweb fabric deployment tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
"""

from fabric.api import *
from fabric.operations import prompt
from fabtools import require
from fabtools.postgres import database_exists, create_database, create_user
from fabtools.python import install_requirements

from . import db
from . import rabbitmq


# Application name
env.app_name = 'ideweb'
# Application user
env.app_user = env.app_name
# App installation directory
env.app_dir = '/var/www/apps/%(app_name)s' % env
# Config file to use
env.config_file = 'deploy/config.py'
# Git remote to clone/pull from
env.git_remote = 'git@github_cdeweb:mcs07/ideweb.git'
# Database user
env.database_user = env.app_name
# Database name
env.database_name = env.app_name
# RabbitMQ user
env.rabbitmq_user = env.app_name
# RabbitMQ vhost
env.rabbitmq_vhost = '%(app_name)s_vhost' % env


@task
def dev():
    """Development server connection details."""
    env.user = 'vagrant'
    env.hosts = ['192.168.33.10']


@task
def prod():
    """Production server connection details."""
    env.user = 'root'
    env.hosts = ['chemdataextractor.org']



@task
def setup():
    """Initial setup - create application user, database, install package dependencies."""
    require.user(env.app_user, group='www-data', system=True, create_home=True)
    require.postgres.server()
    rabbitmq.server()
    require.nginx.server()
    require.deb.packages(['libxml2-dev', 'libxslt1-dev', 'python-dev', 'libffi-dev', 'zlib1g-dev', 'libjpeg-dev'])
    setup_postgres()
    setup_rabbitmq()


@task
def setup_postgres():
    """Initial postgres setup."""
    if not db.user_exists(env.database_user):
        if 'database_pw' not in env:
            prompt('PostgreSQL database password:', key='database_pw')
        create_user(env.database_user, password=env.database_pw, encrypted_password=True)
    if not database_exists(env.database_name):
        create_database(env.database_name, env.database_user)


@task
def setup_rabbitmq():
    """Initial RabbitMQ setup."""
    if 'rabbitmq_pw' not in env:
        prompt('RabbitMQ password:', key='rabbitmq_pw')
    rabbitmq.require_user(env.rabbitmq_user, env.rabbitmq_pw)
    rabbitmq.require_vhost(env.rabbitmq_vhost)
    sudo('rabbitmqctl set_permissions -p %(rabbitmq_vhost)s %(rabbitmq_user)s ".*" ".*" ".*"' % env)
    require.service.started('rabbitmq-server')


@task
def setup_opsin():
    """Initial OPSIN setup."""
    require.deb.packages(['openjdk-7-jre'])
    with cd('/opt'):
        require.file(url='https://bitbucket.org/dan2097/opsin/downloads/opsin-2.1.0-jar-with-dependencies.jar')
        require.file(
            path='/opt/opsin',
            contents='#!/bin/bash\nexec java  -jar /opt/opsin-2.1.0-jar-with-dependencies.jar "$@"\n',
            mode='755'
        )


# @task
# def setup_rdkit():
#     """Initial RDKit setup."""
#     require.deb.packages([
#         'build-essential', 'python-numpy', 'cmake', 'python-dev', 'sqlite3', 'libsqlite3-dev', 'libboost-dev',
#         'libboost-system-dev', 'libboost-thread-dev', 'libboost-serialization-dev', 'libboost-python-dev',
#         'libboost-regex-dev', 'wget'
#     ])
#     with cd('/opt'):
#         require.file(url='https://github.com/rdkit/rdkit/archive/Release_2016_03_1.tar.gz')
#         sudo('tar -xvf Release_2016_03_1.tar.gz')

    # Too lazy, just ran manually on the production machine...
    # cd /opt
    # sudo wget https://github.com/rdkit/rdkit/archive/Release_2016_03_1.tar.gz
    # sudo tar -xvf Release_2016_03_1.tar.gz
    # sudo mv rdkit-Release_2016_03_1 rdkit_2016_03_1

    # sudo -i
    # export RDBASE=/opt/rdkit_2016_03_1
    # export LD_LIBRARY_PATH=/opt/rdkit_2016_03_1/lib:$LD_LIBRARY_PATH
    # export PYTHONPATH=/opt/rdkit_2016_03_1:$PYTHONPATH
    # export JAVA_HOME=/usr/lib/jvm/java-8-oracle
    #
    #
    # mkdir $RDBASE/build
    # cd $RDBASE/build
    # cmake -DRDK_BUILD_THREADSAFE_SSS=ON -DRDK_TEST_MULTITHREADED=ON -DRDK_BUILD_AVALON_SUPPORT=ON -DRDK_BUILD_INCHI_SUPPORT=ON ..
    # make
    # make install


# TODO: libpng? PIL deps.. cairo

@task
def deploy():
    """Deploy everything."""
    deploy_app()
    install_dependencies()
    deploy_config()
    deploy_nginx()
    deploy_celery()


@task
def deploy_app():
    """Deploy app by cloning from github repository."""
    require.git.working_copy(env.git_remote, path=env.app_dir, update=True, use_sudo=True)
    require.files.directory(env.app_dir, group='www-data', use_sudo=True)


@task
def install_dependencies():
    """Ensure all dependencies listed in requirements.txt are installed."""
    with cd(env.app_dir):
        install_requirements('requirements.txt', use_sudo=True)


@task
def deploy_config():
    """Deploy config file to Flask instance folder."""
    require.files.directory('%s/instance' % env.app_dir, use_sudo=True)
    require.file('%(app_dir)s/instance/config.py' % env, source='%(config_file)s' % env, use_sudo=True, group='www-data')


@task
def deploy_gunicorn():
    """Deploy gunicorn service."""
    require.files.template_file(
        '/etc/init/%(app_name)s.conf' % env,
        template_source='deploy/gunicorn.conf',
        context=dict(app_user=env.app_user, app_name=env.app_name, app_dir=env.app_dir)
    )
    require.service.started(env.app_name)


@task
def deploy_nginx():
    """Deploy nginx site configuration and enable site."""
    require.nginx.site(
        env.app_name,
        template_source='deploy/nginx.conf',
        host='chemdataextractor.org',
        app_name=env.app_name,
        docroot=env.app_dir
    )
    require.nginx.enabled(env.app_name)


@task
def deploy_celery():
    """Deploy celery service scripts to appropriate location."""
    require.file('/etc/init.d/%(app_name)s-celeryd' % env, source='deploy/celeryd' % env, use_sudo=True, mode='755')
    require.files.template_file(
        '/etc/default/%(app_name)s-celeryd' % env,
        template_source='deploy/celeryd-default' % env,
        context=dict(app_name=env.app_name, app_dir=env.app_dir),
        use_sudo=True
    )
    sudo('update-rc.d %(app_name)s-celeryd defaults' % env)
    require.directory('/var/log/%(app_name)s' % env, use_sudo=True, owner=env.app_user, group='www-data')
    require.directory('/var/run/%(app_name)s' % env, use_sudo=True, owner=env.app_user, group='www-data')


@task
def start():
    """Start services for gunicorn, nginx, and celeryd."""
    require.service.started(env.app_name)
    require.service.started('nginx' % env)
    require.service.started('%(app_name)s-celeryd' % env)


@task
def restart():
    """Restart services for gunicorn, nginx, and celeryd."""
    require.service.restarted(env.app_name)
    require.service.restarted('nginx' % env)
    require.service.restarted('%(app_name)s-celeryd' % env)
