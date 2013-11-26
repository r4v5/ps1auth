# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
sudo apt-get update
#sudo apt-get -y upgrade

#install dependencies
sudo apt-get -y install build-essential python-dev postgresql git postgresql-server-dev-all libldap2-dev libsasl2-dev python-pip libacl1-dev

#build samba
wget 'http://ftp.samba.org/pub/samba/samba-latest.tar.gz'
tar -xvzf samba-latest.tar.gz
cd samba-*
./configure
make
sudo make install

#download startup script
sudo wget -O /etc/init/samba-ad-dc.conf 'http://anonscm.debian.org/gitweb/?p=pkg-samba/samba.git;a=blob_plain;f=debian/samba-ad-dc.upstart;hb=HEAD'
# patch startup script
sudo sed -i 's|exec samba -D|exec /usr/local/samba/sbin/samba -D|g' /etc/init/samba-ad-dc.conf
sudo /usr/local/samba/bin/samba-tool domain provision --realm=vagrant.lan --domain=VAGRANT --server-role=dc --use-rfc2307 --adminpass=aeng3Oog
sudo service samba-ad-dc start
cd ..

#install python packages
sudo pip install -r /vagrant/requirements/local.txt

# environment variables
echo "export AD_URL=ldap://localhost" >> .bashrc
echo "export AD_DOMAIN=VAGRANT" >> .bashrc
echo "export AD_BASEDN=CN=Users,DC=vagrant,DC=lan" >> .bashrc
echo "export AD_BINDDN=Administrator@VAGRANT" >> .bashrc
echo "export AD_BINDDN_PASSWORD=aeng30og" >> .bashrc
echo "export ZOHO_AUTHTOKEN=deesohshoayie6PiGoGaghi6thiecaingai2quab2aoheequ8vahsu1phu8ahJio" >> .bashrc
echo "export PAYPAL_RECEIVER_EMAIL=money@vagrant.lan" >> .bashrc
SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision "shell", inline: $script
end
