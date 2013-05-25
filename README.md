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
    pip install -r requirements.txt

In "conf/local_settings.py"
--------------------------

    AUTHENTICATION_BACKENDS = (
            'accounts.backends.PS1Backend',
    )

    AD_URL = 'ldaps://host'
    AD_DOMAIN = 'DOMAIN'
    AD_BASEDN = 'CN=Users,DC=host'
    AD_BINDDN = 'admin@DOMAIN'
    AD_BINDDN_PASSWORD = 'admin_password'

Create Tables
-------------

    ./manage.py syncdb
    
Running
-------

    ./manage.py runserver
