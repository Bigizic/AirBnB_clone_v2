#!/usr/bin/env bash
# bash script that prepares a web server

sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx FULL'

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

touch /data/web_static/releases/test/index.html

if [ -L /data/web_static/current ]; then # delte symbolic link
	sudo rm /data/web_static/current
fi

sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"

if ! grep -q "location /hbnb_static/" "$config_file"; then
	sudo tee -a "$config_file" <<EOF
	location /static/ {
		alias /var/www/app/static/;
		autoindex off;
	}
EOF
fi

sudo systemctl restart nginx
