PS1 Member Access System
========================

authentication handler for Pumping Station one


Getting Started
===============

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ./manage.py syncdb
    ./manage.py runserver
    
In a browser navigate to http://localhost:8000

You can perform further custimizations in conf/local_settings.py

    AUTHENTICATION_BACKENDS = (
            'accounts.backends.PS1Backend',
    )

    AD_URL = 'ldaps://host'
    AD_DOMAIN = 'DOMAIN'
    AD_BASEDN = 'CN=Users,DC=host'
    AD_BINDDN = 'admin@DOMAIN'
    AD_BINDDN_PASSWORD = 'admin_password'

