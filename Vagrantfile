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
sudo pacman -Syu --noconfirm

# Install Dependencies 
#sudo apt-get -y install build-essential python-dev postgresql git postgresql-server-dev-all libldap2-dev libsasl2-dev python-pip libacl1-dev
sudo pacman -S --noconfirm --needed postgresql python2-virtualenv samba

#setup Samba
sudo samba-tool domain provision --realm=vagrant.lan --domain=${AD_DOMAIN} --server-role=dc --use-rfc2307 --adminpass=${AD_BINDDN_PASSWORD}
sudo systemctl start samba
sudo systemctl enable samba

# Set Shell Environment Variables
echo "export AD_URL=${AD_URL}" >> .bashrc
echo "export AD_DOMAIN=${AD_DOMAIN}" >> .bashrc
echo "export AD_BASEDN=${AD_BASEDN}" >> .bashrc
echo "export AD_BINDDN=${AD_BINDDN}" >> .bashrc
echo "export AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}" >> .bashrc
echo "export SECRET_KEY=${SECRET_KEY}" >> .bashrc
echo "export ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}" >> .bashrc
echo "export PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}" >> .bashrc

#  Setup Database
chmod 755 /home/vagrant
sudo -u postgres initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres createuser --superuser vagrant
createdb ps1auth


# bootstrap app
virtualenv2 venv
venv/bin/pip install -r /vagrant/requirements/local.txt
sudo pip2 install -r /vagrant/requirements/local.txt
venv/bin/python /vagrant/manage.py syncdb
venv/bin/python /vagrant/manage.py migrate

# Upstart
echo "author 'vagrant'" > /etc/init/ps1auth.conf
echo "description 'vagrant development ps1 authentication server'" >> /etc/init/ps1auth.conf
echo "start on vagrant-mounted" >> /etc/init/ps1auth.conf
echo "stop on shutdown" >> /etc/init/ps1auth.conf
echo "console log" >> /etc/init/ps1auth.conf
echo "respawn" >> /etc/init/ps1auth.conf
echo "respawn limit 10 5" >> /etc/init/ps1auth.conf
echo "setuid vagrant" >> /etc/init/ps1auth.conf
echo "setgid vagrant" >> /etc/init/ps1auth.conf
echo "env AD_URL='${AD_URL}'" >> /etc/init/ps1auth.conf
echo "export AD_URL" >> /etc/init/ps1auth.conf
echo "env AD_BASEDN='${AD_BASEDN}'" >> /etc/init/ps1auth.conf
echo "export AD_BASEDN" >> /etc/init/ps1auth.conf
echo "env AD_BINDDN='${AD_BINDDN}'" >> /etc/init/ps1auth.conf
echo "export AD_BINDDN" >> /etc/init/ps1auth.conf
echo "env AD_BINDDN_PASSWORD='${AD_BINDDN_PASSWORD}'" >> /etc/init/ps1auth.conf
echo "export AD_BINDDN_PASSWORD" >> /etc/init/ps1auth.conf
echo "env SECRET_KEY='${SECRET_KEY}'" >> /etc/init/ps1auth.conf
echo "export SECRET_KEY" >> /etc/init/ps1auth.conf
echo "env ZOHO_AUTHTOKEN='${ZOHO_AUTHTOKEN}'" >> /etc/init/ps1auth.conf
echo "export ZOHO_AUTHTOKEN" >> /etc/init/ps1auth.conf
echo "env PAYPAL_RECEIVER_EMAIL='${PAYPAL_RECEIVER_EMAIL}'" >> /etc/init/ps1auth.conf
echo "export PAYPAL_RECIEVER_EMAIL" >> /etc/init/ps1auth.conf
echo "env AD_DOMAIN='${AD_DOMAIN}'" >> /etc/init/ps1auth.conf
echo "export AD_DOMAIN" >> /etc/init/ps1auth.conf
echo "exec /usr/bin/python /vagrant/manage.py runserver 0.0.0.0:8000" >> /etc/init/ps1auth.conf
sudo service ps1auth start
SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "archlinux-x86_64"
  config.vm.box_url = "http://cloud.terry.im/vagrant/archlinux-x86_64.box"
  config.vm.provision "shell", inline: $script
  #config.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true
  #config.vm.network "private_network", ip: "192.168.50.4"
end
