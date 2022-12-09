#!/bin/bash
#
# Will install fuhttpd in /usr/local/bin and service in /etc/systemd/system
WEBROOT="/var/www/html/"

cont () {
        #Reads from input and returns true/false
        # Ex: cont && do something
#        [ -z "$1" ] && 1="Continue?"
        read -p "$1? (y/n): " -n 1 -r
        echo    # (optional) move to a new line
        if [[ $REPLY =~ ^[Yy]$ ]]; then
                return
        else
                false
        fi
}

INSTALLDIR="/usr/local/bin"

[ -f fuhttpd.py ] && sudo cp fuhttpd.py "$INSTALLDIR" || echo "fuhttpd.py not found! Where are we running this from?"
[ -f cert.pem ] && sudo cp cert.pem "$INSTALLDIR" || echo "No cert.pem, please generate!"
[ -f key.pem ] && sudo cp key.pem "$INSTALLDIR" || echo "No key.pem, please generate!"

sudo useradd --system --shell=/usr/sbin/nologin www-data || echo "ERROR! User already exists...?"

sudo chown www-data:www-data "$INSTALLDIR"/cert.pem && sudo chmod 640 "$INSTALLDIR"/cert.pem || echo "No cert.pem, please generate!"
sudo chown www-data:www-data "$INSTALLDIR"/key.pem && sudo chmod 640 "$INSTALLDIR"/key.pem || echo "No key.pem, please generate!"


sudo systemctl stop fuhttpd.service && echo "Old service stopped!" || echo "No service stopped"

[ ! -d "$WEBROOT" ] && echo "Default webroot: "$WEBROOT" does not exist!" && cont "Create?" && sudo mkdir -p "$WEBROOT" && sudo chown -R www-data:www-data "$WEBROOT"

echo "Do you want to run HTTPS, plain HTTP or both?"

cont "Activate HTTPS on 443" && [ -f fuhttpd.service ] && sudo cp fuhttpd.service /etc/systemd/system && sudo systemctl daemon-reload && sudo systemctl enable fuhttpd.service && echo "Service enabled. Run systemctl start fuhttpd, to start." && cont "Start service now" && sudo systemctl start fuhttpd.service

cont "Activate plain HTTP on 80" && [ -f plain-fuhttpd.service ] && sudo cp plain-fuhttpd.service /etc/systemd/system && sudo systemctl daemon-reload && sudo systemctl enable plain-fuhttpd.service && echo "Service enabled. Run systemctl start fuhttpd, to start." && cont "Start service now" && sudo systemctl start plain-fuhttpd.service
