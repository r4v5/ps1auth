from fabric.api import *
from cuisine import *

env.hosts = ['arbitrarion.com']

def deploy():
    with cd('/srv/http/arbitrarion.com/app/'):
        run('git pull')
        with prefix('workon ps1auth'):
            run('./manage.py syncdb --noinput')
            run('./manage.py migrate --noinput')
            run('./manage.py collectstatic --noinput')
            run('killall /home/hef/.virtualenvs/ps1auth/bin/python2')

