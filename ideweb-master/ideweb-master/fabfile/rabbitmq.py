# -*- coding: utf-8 -*-
"""
fabfile.rabbitmq
~~~~~~~~~~~~~~~~

RabbitMQ fabric tasks.
 
"""

from fabric.api import *
from fabtools import require


def server():
    """Require a RabbitMQ server to be installed and running."""
    require.deb.source('rabbitmq', 'http://www.rabbitmq.com/debian/', 'testing', 'main')
    require.deb.key('056E8E56', url='https://www.rabbitmq.com/rabbitmq-signing-key-public.asc')
    require.deb.package('rabbitmq-server')
    require.service.started('rabbitmq-server')


def user_exists(name):
    """Check if a RabbitMQ user exists."""
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        users = sudo('rabbitmqctl list_users').splitlines()[1:-1]
    names = [u.split()[0] for u in users]
    return name in names


def create_user(name, password):
    """Create a RabbitMQ user."""
    sudo('rabbitmqctl add_user %s %s' % (name, password))


def require_user(name, password):
    """Require the existence of a RabbitMQ user."""
    if not user_exists(name):
        create_user(name, password)


def vhost_exists(vhost):
    """Check if a RabbitMQ vhost exists."""
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        vhosts = sudo('rabbitmqctl list_vhosts').splitlines()[1:-1]
    return vhost in vhosts


def create_vhost(vhost):
    """Create a RabbitMQ vhost."""
    sudo('rabbitmqctl add_vhost %s' % vhost)


def require_vhost(vhost):
    """Require the existence of a RabbitMQ vhost."""
    if not vhost_exists(vhost):
        create_vhost(vhost)
