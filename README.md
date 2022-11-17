# fuhttpd
Small and simple http daemon in python.

### Usage:
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
Generate certs:
```
./generate_keys.sh
or:
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```
