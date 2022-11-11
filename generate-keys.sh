#!/bin/bash
# Generate a pair of generic ssl cert and keys
openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365