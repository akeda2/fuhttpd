#!/bin/bash
# Generate a pair of generic ssl cert and keys
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
# Copy the cert and key to /usr/local/share/ca-certificates:
sudo cp cert.pem /usr/local/share/ca-certificates/
sudo cp key.pem /usr/local/share/ca-certificates/