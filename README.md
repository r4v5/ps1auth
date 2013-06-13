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
    pip install -r requirements.txt

Configuring
===========

Development
-----------

In conf/local\_settings.py

    AD_URL = 'ldaps://host'
    AD_DOMAIN = 'DOMAIN'
    AD_BASEDN = 'CN=Users,DC=host'
    AD_BINDDN = 'admin@DOMAIN'
    AD_BINDDN_PASSWORD = 'admin_password'

Production
----------

In conf/local\_settings.py

    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    EMAIL_BACKEND = 'django.core.mail.backends.smptp.EmailBackend'
    SERVER_EMAIL = 'no-reply@host'
    ADMINS = (
        ('you', 'you@host'),
    )
    MANAGERS = ADMINS
    ALLOWED_HOSTS = ['hostname']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_pscopg2'
            'NAME': 'ps1auth'
            'USER': 'you'
        }
    }

    AD_URL = 'ldaps://host'
    AD_DOMAIN = 'DOMAIN'
    AD_BASEDN = 'CN=Users,DC=host'
    AD_BINDDN = 'admin@DOMAIN'
    AD_BINDDN_PASSWORD = 'admin_password'



Initializing
============

Create Tables
-------------

    ./manage.py syncdb
    ./manage.py migrate
    
Running
-------

    ./manage.py runserver
