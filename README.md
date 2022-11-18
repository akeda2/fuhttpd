# fuhttpd
Small and simple http daemon in python.

### Usage:
```
python3 fuhttpd.py
python3 fuhttpd.py /path/to/web/root

Plain HTTP:
python3 fuhttpd.py -p/--plain
python3 fuhttpd.py -p/--plain /path/to/web/root
```
### Systemd service:
```
Edit fuhttpd.service with your path then:
sudo cp fuhttpd.service /etc/systemd/system
sudo systemctl enable fuhttpd.service
sudo systemctl start fuhttpd.service
```
### Generate certs:
```
./generate_keys.sh
or:
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
Copy or symlink these to your working directory or run install.sh if you like the defaults (/usr/local/bin).
```

## Legacy:
HTTPS using SSLContext:
```
With threading:
python3 tsfuhttpd.py
Without:
python3 sfuhttpd.py
```
Using plain HTTP:
```
With threading:
python3 tfuhttpd.py
Without:
python3 fuhttpd.py
```
