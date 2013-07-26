P1 Member Access System
========================

Getting Started
===============

On Arch Linux
-------------

    sudo pacman -S base-devel python2-virtualenv

On Ubuntu 12.04
---------------

    sudo apt-get install libldap-dev libpq-dev python-dev libsasl2-dev

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
    export ZOHO_AUTHTOKEN='your_auth_token'
    
Get your zoho authtoken [here](https://accounts.zoho.com/apiauthtoken/create?SCOPE=ZohoCRM/crmapi)

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
    s.domain = u'localhost:8000'
    s.name = u'PS1 Auth Dev Site'
    s.save()
    quit()
    
Running
-------

    ./manage.py runserver

