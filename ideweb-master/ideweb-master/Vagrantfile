Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.hostname = "cdeweb"
  config.vm.synced_folder "./", "/var/www/apps/cdeweb", create: true, group: "www-data", owner: "www-data"

  # Configure VM name and increase RAM
  config.vm.provider "virtualbox" do |vb|
    vb.name = "cdeweb VM"
    vb.memory = "4096"
  end
end
