#!/bin/bash
#
# Will install fuhttpd in /usr/local/bin and service in /etc/systemd/system

[ -f fuhttpd.py ] && sudo cp fuhttpd.py /usr/local/bin/
[ -f cert.pem ] && sudo cp cert.pem /usr/local/bin/ || echo "No cert.pem, please generate!"
[ -f key.pem ] && sudo cp key.pem /usr/local/bin/ || echo "No key.pem, please generate!"
chmod a+r cert.pem || echo "No cert.pem, please generate!"
chmod a+r key.pem || echo "No key.pem, please generate!"
[ -f fuhttpd.service ] && sudo cp fuhttpd.service /etc/systemd/system && sudo systemctl enable fuhttpd.service && echo "Service enabled, run systemctl start fuhttpd, to start"
