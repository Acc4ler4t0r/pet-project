Мой 2ой pet-проект (vagrant+python+postgresql+docker)

1) Vagrantfile нужно засунуть в какую-либо папку на основной машине, в PS перейти в неё (cd c:/) и запустить командой *vagrant up*. Послу успешного запуска необходимо подключиться к машине (vagrant ssh *имя_машины_из_файла*)

2) mkdir myapp в корне машины (home/vagrant/myapp)

  2.1) Можно воспользоваться init.sql для создания необходимой БД

3) В созданной папке должен находиться main.py. В этой же папке должна находиться папка templates (home/vagrant/myapp/templates) с HTML-формами

4) Добавить nginx, docker-compose

   
