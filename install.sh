#!/bin/bash
#
# Will install fuhttpd in /usr/local/bin and service in /etc/systemd/system

[ -f fuhttpd.py ] && sudo cp fuhttpd.py /usr/local/bin/
[ -f cert.pem ] && sudo cp cert.pem /usr/local/bin/
[ -f key.pem ] && sudo cp key.pem /usr/local/bin/
chmod a+r cert.pem
chmod a+r key.pem
[ -f fuhttpd.service ] && sudo cp fuhttpd.service /etc/systemd/system && sudo systemctl enable fuhttpd.service
