# fuhttpd
Small and simple http daemon in python.

### Usage:
HTTPS using SSLContext:
```
python3 sfuhttpd.py
```
HTTPS using ssl.wrap_socket:(old, just for reference)
```
python3 old_sfuhttpd.py
```
Using plain HTTP:
```
python3 fuhttpd.py
```
Generate certs:
```
./generate_keys.sh
or:
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```
