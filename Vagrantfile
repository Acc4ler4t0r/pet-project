ENV['VAGRANT_SERVER_URL'] = 'https://vagrant.elab.pro' # зеркало для РФ

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_check_update = false

  # ==========================================
  # Машина 1: Main host
  # ==========================================

  config.vm.define "main_host" do |main_host|
    main_host.vm.hostname = "main-host"
    main_host.vm.network "private_network", ip: "192.168.13.13"
    
    # ресурсы VirtualBox
 
    main_host.vm.provider "virtualbox" do |vb|
      vb.memory = "1536"
      vb.cpus = 1
      vb.name = "main-host-server"
    end
  end
end