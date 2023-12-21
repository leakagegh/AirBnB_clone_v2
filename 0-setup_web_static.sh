#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary folders if they don't exist
folders=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
for folder in "${folders[@]}"; do
    if [ ! -d "$folder" ]; then
        mkdir -p "$folder"
    fi
done

# Create a fake HTML file
echo "<html><head></head><body>Hello World!/body></html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
if [ -L "/data/web_static/current" ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
new_config="location /hbnb_static {\n    alias /data/web_static/current/;\n}\n"
sed -i "/server_name _;/a $new_config" "$config_file"

# Restart Nginx
service nginx restart

exit 0
