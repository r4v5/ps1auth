# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
sudo apt-get update
#sudo apt-get -y upgrade
sudo apt-get -y install build-essential python-dev postgresql git postgresql-server-dev-all libldap2-dev libsasl2-dev python-pip
wget 'http://ftp.samba.org/pub/samba/samba-latest.tar.gz'
tar -xvzf samba-latest.tar.gz
cd samba-*
./configure
make
sudo make install
cd ..
sudo pip install -r /vagrant/requirements/local.txt
SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "Precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision "shell", inline: $script
end
