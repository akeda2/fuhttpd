#!/bin/bash
#
# Will install fuhttpd in /usr/local/bin and service in /etc/systemd/system

INSTALLDIR="/usr/local/bin"

[ -f fuhttpd.py ] && sudo cp fuhttpd.py "$INSTALLDIR" || echo "fuhttpd.py not found! Where are we running this from?"
[ -f cert.pem ] && sudo cp cert.pem "$INSTALLDIR" || echo "No cert.pem, please generate!"
[ -f key.pem ] && sudo cp key.pem "$INSTALLDIR" || echo "No key.pem, please generate!"
sudo chmod a+r "$INSTALLDIR"/cert.pem || echo "No cert.pem, please generate!"
sudo chmod a+r "$INSTALLDIR"/key.pem || echo "No key.pem, please generate!"
sudo useradd --system --shell=/usr/sbin/nologin www-data
[ -f fuhttpd.service ] && sudo cp fuhttpd.service /etc/systemd/system && sudo systemctl enable fuhttpd.service && echo "Service enabled, run systemctl start fuhttpd, to start"
