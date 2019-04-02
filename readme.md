initial password raspberry

sudo raspi-config

sudo dpkg-reconfigure tzdata
sudo apt-get update
sudo apt-get upgrade



###### Install Apache2 Webserver:
```
sudo apt-get install apache2
(Rufe IP-Addr auf)
```
###### Install Mysql:
```
sudo apt-get install mysql-server
Give root pw for mysql

Check mysql : mysql -u root -p
```
###### Install php
sudo apt-get install php7.0

sudo apt-get install php-mysql

add test php file to dir /var/www/html/

###### Install phpmyadmin
```
sudo apt-get install phymyadmin
user: phpmyadmin
pw: pi_root1
```
