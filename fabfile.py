#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import run, env, cd, put, sudo, abort, roles
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm


env.user = 'group'
#env.hosts = ['210.44.176.241:2722',]
env.roledefs = {
        'py-ubuntu': ['210.44.176.241:2722']
        }

# 项目目录
PROJECT_HOME = '/home/group/pahchina'
# Supervisor中的项目名称
PROJECT_NAME_IN_SUPERVISOR = 'pahchina'
# 部署的分支
DEPLOY_BARNCH = 'zhwei'


@roles('py-ubuntu')
def deploy(branch=DEPLOY_BARNCH):
    """远程部署
    """
    with cd(PROJECT_HOME):
        ret = run('git pull origin %s' % branch)
        if ret.failed and not confirm('Pull from origin %s Failed, Continue anyway ?') % branch:
            print(yellow('=== git pull log'))
            print(ret)
            print(yellow('=== git status log'))
            run('git status')
            abort(red('Aborting at pull from origin'))
        print(green('Pull from branch %s successfully') % branch)
        sudo('supervisorctl restart %s' % PROJECT_NAME_IN_SUPERVISOR)
        print(green('Deploy Successfully !!'))


def put_sshkey():
    """push ssh key to server
    """
    with cd('/tmp'):
        put('id_rsa.pub.master', 'id_rsa.pub.master')
        run('cat id_rsa.pub.master >> ~/.ssh/authorized_keys')
