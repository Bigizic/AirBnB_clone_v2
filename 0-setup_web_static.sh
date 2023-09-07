#!/usr/bin/env bash
# bash script that prepares a web server

sudo apt update
if ! dpkg -l | grep -q "nginx"; then
	sudo apt install nginx -y
	sudo ufw allow 'Nginx FULL'
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# touch /data/web_static/releases/test/index.html
echo "test page" | sudo tee /data/web_static/releases/test/index.html > /dev/null

if [ -L /data/web_static/current ]; then # delte symbolic link
	sudo rm /data/web_static/current
fi

sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"

if ! grep -q "location /hbnb_static/" "$config_file"; then
	echo "location /hbnb_static/ {" | sudo tee -a "$config_file"
	echo "    alias /data/web_static/current/;" | sudo tee -a "$config_file"
	echo "    autoindex off;" | sudo tee -a "$config_file"
	echo "}" | sudo tee -a "$config_file"
fi

sudo systemctl restart nginx
