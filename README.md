PS1 Member Access System
========================

Getting Started
===============

On Ubuntu
---------

    sudo apt-get install libldap-dev

On All Platforms
----------------

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements/local.txt

Environment Variables
---------------------

    AD_URL = 'ldaps://host'
    AD_DOMAIN = 'DOMAIN'
    AD_BASEDN = 'CN=Users,DC=host'
    AD_BINDDN = 'admin@DOMAIN'
    AD_BINDDN_PASSWORD = 'admin_password'

Database
--------

Install and configure postgresql for your system.
[Arch](https://wiki.archlinux.org/index.php/PostgreSQL)

    createuser -s -U postgres $USER
    createdb ps1auth

Create Tables
-------------

    ./manage.py syncdb
    ./manage.py migrate
    
Running
-------

    ./manage.py runserver

