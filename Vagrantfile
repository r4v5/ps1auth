# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# Set Environment Variables
export AD_URL="ldap://localhost"
export AD_DOMAIN="VAGRANT"
export AD_BASEDN="CN=Users,DC=vagrant,DC=lan"
export AD_BINDDN="Administrator@VAGRANT"
export AD_BINDDN_PASSWORD="aeng3Oog"
export SECRET_KEY="deesohshoayie6PiGoGaghi6thiecaingai2quab2aoheequ8vahsu1phu8ahJio"
export ZOHO_AUTHTOKEN="add-your-auth-token"
export PAYPAL_RECEIVER_EMAIL="money@vagrant.lan"

# Update the System
#sudo pacman -Syu --noconfirm
sudo pacman -Syy

# Setup locale.gen
cat << EOF > /etc/locale.gen
en_US.UTF-8 UTF-8  
en_US ISO-8859-1  
EOF
locale-gen

# Install Dependencies 
sudo pacman -S --noconfirm --needed postgresql python2-virtualenv samba

# Setup Samba
sudo samba-tool domain provision --realm=vagrant.lan --domain=${AD_DOMAIN} --server-role=dc --use-rfc2307 --adminpass=${AD_BINDDN_PASSWORD}
sudo systemctl start samba
sudo systemctl enable samba

# Set Shell Environment Variables
cat << EOF >> .bashrc
export AD_URL=${AD_URL}
export AD_DOMAIN=${AD_DOMAIN}
export AD_BASEDN=${AD_BASEDN}
export AD_BINDDN=${AD_BINDDN}
export AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}
export SECRET_KEY=${SECRET_KEY}
export ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}
export PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}
source venv/bin/activate
EOF

#  Setup Database
chmod 755 /home/vagrant
sudo -u postgres initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres createuser --superuser vagrant
sudo -u vagrant createdb ps1auth

# Bootstrap App

sudo -u vagrant virtualenv2 venv
sudo -u vagrant venv/bin/pip install -r /vagrant/requirements/local.txt
sudo -u vagrant venv/bin/pip install gunicorn
sudo -u vagrant -E venv/bin/python /vagrant/manage.py syncdb
sudo -u vagrant -E venv/bin/python /vagrant/manage.py migrate


# Setup systemd environment file
cat << EOF > /home/vagrant/ps1auth.conf
AD_URL=${AD_URL}
AD_DOMAIN=${AD_DOMAIN}
AD_BASEDN=${AD_BASEDN}
AD_BINDDN=${AD_BINDDN}
AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}
SECRET_KEY=${SECRET_KEY}
ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}
PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}
EOF


# Systemd Service File
cat << EOF > /etc/systemd/system/ps1auth.service
[Unit]
Description=PS1 Auth (Member's site)

[Service]
User=vagrant
WorkingDirectory=/vagrant
#ExecStart=/home/vagrant/venv/bin/gunicorn --debug --log-level debug ps1auth.wsgi:application
ExecStart=/home/vagrant/venv/bin/python manage.py 0.0.0.0:8001
EnvironmentFile=-/home/vagrant/ps1auth.conf

[Install]
WantedBy=multi-user.target
EOF

# Systemd Socket File
cat << EOF > /etc/systemd/system/ps1auth.socket
[Unit]
Description=PS1Auth (Member's Site) Socket

[Socket]
ListenStream=0.0.0.0:8001

[Install]
WantedBy=sockets.target
EOF

# Configure App to Start Automatically
#sudo systemctl start ps1auth.socket
#sudo systemctl enable ps1auth.socket
systemctl start ps1auth
systemctl enable ps1auth

SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "archlinux-x86_64"
  config.vm.box_url = "http://cloud.terry.im/vagrant/archlinux-x86_64.box"
  config.vm.provision "shell", inline: $script
  config.vm.network "forwarded_port", guest: 8001, host: 8001, auto_correct: true
end
