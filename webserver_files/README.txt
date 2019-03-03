
install web server with php

copy playerinfo.php file to webserver root directory (typically /var/www/html/)

browse to webserver_ip_address/playerinfo.php
page will automatically reload every five seconds

playerinfo.php will read it's data from a file located at /var/www/html/tmp/playerlist.txt.  Each line of data in that file must be in the following format:

Player Name,heartrate,bodytemperature

