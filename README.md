# fuhttpd
Small and simple http daemon in python.

### Usage:
Using ssl.wrap_socket:
```
python3 fuhttpd.py
```
Using SSLContext:
```
python3 sfuhttpd.py
```
Generate certs:
```
./generate_keys.sh
or:
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```
