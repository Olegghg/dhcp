#!/bin/bash
ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa
var=$(cat ~/.ssh/id_rsa.pub)
sed -i "s|ssh-rsa ...|$var|" tftp/tftpboot/ce/preseed.cfg
apt install -y isc-dhcp-server
cp -rf dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf
cp -f dhcp/default /etc/default/isc-dhcp-server
apt install -y tftpd-hpa pxelinux syslinux
cp -rf tftp/default /etc/default/tftpd-hpa
cp -rf tftp/tftpboot /srv/

apt install -y apache2
cp -rf http/repo /srv
ln -s /srv/repo /var/www/html/
cp -rf http/site.conf /etc/apache2/sites-enabled/000-default.conf

systemctl restart isc-dhcp-server
systemctl restart tftpd-hpa
systemctl restart apache2

apt install -y ansible
