# pxe
1. Установка git

apt install git
git clone https://github.com/Olegghg/pxe.git
cd pxe

2. Редактирование конфигов
2.1. dhcp
В файле dhcp/default указать используемый порт

Пример:
INTERFACESv4="eth1"

В файле dhcp/dhcpd.conf	поменять адресацию

Пример:
next-server 10.10.10.1; - адрес tftp

subnet 10.10.10.0 netmask 255.255.255.0 {
    range 10.10.10.20 10.10.10.250;
    option broadcast-address 10.10.10.255;
    option routers 10.10.10.1;
    option subnet-mask 255.255.255.0;
}

2.2 tftp

В tftp/tftpboot/pxelinux.cfg/default поменять 
- url до preseed.cfg, hostname клиента, domain для клиента  
Пример:

url=tftp://10.10.10.1/ce/preseed.cfg

Поменять tftp/tftpboot/ce/preseed.cfg если есть необходимость



#Далее отредактировать опции в этом файле:

Основные опции:
d-i mirror/protocol string http
d-i mirror/country string manual
d-i mirror/http/hostname string 10.10.10.1 - репозиторий
d-i time/zone string Europe/Moscow
d-i passwd/user-fullname string u
d-i passwd/username string u
d-i passwd/root-password password pass
d-i passwd/root-password-again password pass

3. Распаковка iso, http-репозиторий

Получить iso образ
Примонтировать его в систему:
mount -o loop orel.iso /mnt
mkdir -p http/repo/ce/
cp -r /mnt/* http/repo/ce/
cp /mnt/netinst/linux tftp/tftpboot/ce/
cp /mnt/netinst/initrd.gz tftp/tftpboot/ce/

4. Запуск установки pxe
./install.sh

 