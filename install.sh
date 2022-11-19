#!/bin/bash
#
# Will install fuhttpd in /usr/local/bin and service in /etc/systemd/system
WEBROOT="/var/www/html/"

cont () {
        #Reads from input and returns true/false
        # Ex: cont && do something
        [ -z "$1" ] && 1="Continue?"
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
sudo chmod a+r "$INSTALLDIR"/cert.pem || echo "No cert.pem, please generate!"
sudo chmod a+r "$INSTALLDIR"/key.pem || echo "No key.pem, please generate!"
sudo useradd --system --shell=/usr/sbin/nologin www-data || echo "ERROR! User already exists...?"
sudo systemctl stop fuhttpd.service && echo "Old service stopped!" || echo "No service stopped"
[ ! -d "$WEBROOT" ] && echo "Default webroot: "$WEBROOT" does not exist!" && cont "Create?" && sudo mkdir "$WEBROOT"
[ -f fuhttpd.service ] && sudo cp fuhttpd.service /etc/systemd/system && sudo systemctl daemon-reload && sudo systemctl enable fuhttpd.service && echo "Service enabled. Run systemctl start fuhttpd, to start." && cont "Start service now?" && sudo systemctl start fuhttpd.service