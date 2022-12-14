# fuhttpd
Small and simple http daemon in python using SimpleHTTPRequestHandler.
I would not use this on the open internet...

## Usage:
```
$ python3 fuhttpd.py -h
usage: fuhttpd.py [-h] [-P] [-p PORT] [-d] [path]

fuHTTPd

positional arguments:
  path                  Root directory. If omitted - use current (default:
                        None)

optional arguments:
  -h, --help            show this help message and exit
  -P, --plain           Use plain HTTP (default: False)
  -p PORT, --port PORT  Use custom port (default: None)
  -d, --dirlist         Allow directory listings (default: False)
```
### Examples:
```
HTTPS (default):
python3 fuhttpd.py
python3 fuhttpd.py -p/--port XXXXX
python3 fuhttpd.py /path/to/web/root

Plain HTTP:
python3 fuhttpd.py -P/--plain
python3 fuhttpd.py -P/--plain /path/to/web/root
```
### Installer shell script:
```
Run shell script:
./install.sh

This will set up systemd services for https or http (or both) and optionally start them.
Webroot is "/var/www/html" by default. If your webroot is somewhere else, just maka a symlink.
```
### Systemd service:
```
fuhttpd.service - https on port 443
plain-fuhttpd.service - plain http on port 80

Edit these to your liking, then...:

sudo cp fuhttpd.service /etc/systemd/system
sudo systemctl enable fuhttpd.service
sudo systemctl start fuhttpd.service

...and the same goes for plain-fuhttpd.service.
```
### Generate certs:
```
./generate_keys.sh
or:
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
Copy or symlink these to your working directory or run install.sh if you like the defaults (/usr/local/bin).
```
