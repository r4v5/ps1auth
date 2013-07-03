P1 Member Access System
========================

Getting Started
===============

On Arch Linux
-------------

    sudo pacman -S base-devel python2-virtualenv

On Ubuntu
---------

    sudo apt-get install libldap-dev

On All Platforms
----------------

    virtualenv venv # (virtualenv2 on arch)
    source venv/bin/activate
    pip install -r requirements/local.txt

Environment Variables
---------------------
A good place for these is in $VIRTUAL_ENV/bin/postactivate

    export AD_URL='ldaps://host'
    export AD_DOMAIN='DOMAIN'
    export AD_BASEDN='CN=Users,DC=host'
    export AD_BINDDN='admin@DOMAIN'
    export AD_BINDDN_PASSWORD='admin_password'

Database
--------

Install and configure postgresql for your system.
[Arch](https://wiki.archlinux.org/index.php/PostgreSQL)

    createuser -s -U postgres $USER
    createdb ps1auth



Initializing
============

Create Tables
-------------

    ./manage.py syncdb
    ./manage.py migrate

Set Site name
-------------

    ./manage shell
    from django.contrib.sites.models import Site
    s = Site.objects.get(pk=1)
    s.domain = u'localhost'
    s.name = u'PS1 Auth Dev Site'
    s.save()
    quit()
    
Running
-------

    ./manage.py runserver

