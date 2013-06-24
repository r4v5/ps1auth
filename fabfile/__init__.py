from fabric.api import *
from cuisine import *


def vagrant():
    "Use vagrant for testing"
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.lstrip('IdentityFile').strip(' "')

def setup():
    package_update()
    package_ensure("nginx")
    package_ensure("postgresql")
    upload_file("/etc/nginx/sites_enabled/nginx.conf", "nginx.conf")


def deploy():
    with cd('/srv/http/arbitrarion.com/app/'):
        run('git pull')
        with prefix('source /srv/http/arbitrarion.com/venv/bin/activate'):
            run('./manage.py migrate')
            run('killall /srv/http/arbitrarion.com/venv/bin/python2')

