initial password raspberry

sudo raspi-config

sudo dpkg-reconfigure tzdata
sudo apt-get update
sudo apt-get upgrade



##### Install Apache2 Webserver:
```
sudo apt-get install apache2
(Rufe IP-Addr auf)
```
##### Install Mysql:
```
sudo apt-get install mysql-server
Give root pw for mysql

Check mysql : mysql -u root -p
```
##### Install php
sudo apt-get install php7.0

sudo apt-get install php-mysql

add test php file to dir /var/www/html/

##### Install phpmyadmin
```
sudo apt-get install phymyadmin
user: phpmyadmin
pw: pi_root1
```

##### Install cakephp
curl -s https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
apt-get install php7.0-intl
###### Swap 
```
/bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024
/sbin/mkswap /var/swap.1
/sbin/swapon /var/swap.1
```
composer create-project --prefer-dist cakephp/app my_app_name
