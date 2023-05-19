import re
import subprocess
import os
while True:
    # Запрашиваем данные
    hostname = input("Введите имя хоста: ")
    mac_address = input("Введите MAC-адрес (в формате xx:xx:xx:xx:xx:xx): ")
    ip_address = input("Введите IP-адрес: ")
    groupname = input('Название anible группы (файл /etc/ansible/hosts). Например KS: ')

    #проверка MAC
    mac_regex_format = re.compile(r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")
    if not mac_regex_format.match(mac_address):
        print("Ошибка: MAC-адрес не соответствует формату xx:xx:xx:xx:xx:xx")
        exit(1)

    #Проверка IP
    ip_regex_format = re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    if not ip_regex_format.match(ip_address):
        print("Ошибка: IP-адрес не соответствует формату x.x.x.x, где x от 0 до 255")
        exit(1)

    #Проверка названия группы
    with open("/etc/ansible/hosts", "r") as file:
        ansible_content = file.read()
        group_regex=re.compile(r"\["+groupname+"\]")
    if not group_regex.search(ansible_content):
        print(f"Ошибка: Нет такой группы")
        exit(1)

    # Проверяем, существует ли файл dhcpd.conf
    if not os.path.isfile("/etc/dhcp/dhcpd.conf"):
        print("Файл dhcpd.conf не найден")
        exit(1)

    # Читаем содержимое файла
    with open("/etc/dhcp/dhcpd.conf", "r") as file:
        dhcpd_content = file.read()

    # Создаем регулярные выражения для поиска
    hostname_regex = re.compile(r"host\s+" + re.escape(hostname) + r"\s+\{")
    mac_regex = re.compile(r"hardware ethernet\s+" + re.escape(mac_address) + r";")
    ip_regex = re.compile(r"fixed-address\s+" + re.escape(ip_address) + r";")

    # Проверяем, есть ли совпадения
    if hostname_regex.search(dhcpd_content):
        print("Ошибка: Имя хоста "+hostname+" уже настроено")
    elif mac_regex.search(dhcpd_content):
        print("Ошибка: MAC-адрес "+str(mac_address)+" уже настроен")
    elif ip_regex.search(dhcpd_content):
        print("Ошибка: IP-адрес "+str(ip_address)+" уже настроен")
    else:
        # Если совпадений нет, добавляем новую запись
        with open("/etc/dhcp/dhcpd.conf", "a") as file:
            file.write("\nhost " + hostname + " {\n  hardware ethernet " + mac_address + ";\n  fixed-address " + ip_address + ";\n}")

        print("Запись добавлена")

    # Формируем строку ansible
    ansible_line = "["+groupname+"]\n" + hostname + " ansible_host=" + ip_address + " ansible_user=ansibleuser ansible_ssh_private_key_file=~/.ssh/id_rsa"

    # Записываем строку в файл ansible/hosts.ini
    with open('/etc/ansible/hosts', 'r') as f:
        content = f.read()
    content = content.replace("["+groupname+"]", ansible_line)
    with open('/etc/ansible/hosts', 'w') as f:
        f.write(content)
    #Новая запись?
    nextstr = input("Введите y для создания еще 1 записи: ")
    if nextstr!="y":
        break
try:
    subprocess.check_call(["systemctl", "restart", "isc-dhcp-server"])
    print("Сервис isc-dhcp-server был перезапущен")
except subprocess.CalledProcessError:
    print("Ошибка при перезапуске сервиса isc-dhcp-server")
