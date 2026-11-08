# Указываем наше рабочее зеркало для РФ
ENV['VAGRANT_SERVER_URL'] = 'https://vagrant.elab.pro'

Vagrant.configure("2") do |config|
  # Базовый образ для всех машин
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_check_update = false # Отключаем надоедливые проверки обновлений

  # ==========================================
  # Машина 1: Main host
  # ==========================================
  config.vm.define "main_host" do |main_host|
    main_host.vm.hostname = "main-host"
    # Статический IP-адрес для связи между машинами
    main_host.vm.network "private_network", ip: "192.168.13.13"
    
    # Настройка ресурсов VirtualBox (1.5 ГБ RAM, 1 ядро CPU)
    main_host.vm.provider "virtualbox" do |vb|
      vb.memory = "1536"
      vb.cpus = 1
      vb.name = "main-host-server"
    end
  end
end