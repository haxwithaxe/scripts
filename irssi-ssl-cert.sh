#!/bin/bash

set -e

cd /usr/share/ca-certificates
mkdir gandi.net
cd gandi.net
wget http://crt.gandi.net/GandiStandardSSLCA.crt
openssl x509 -inform der -outform pem < /usr/share/ca-certificates/gandi.net/GandiStandardSSLCA.crt > GandiStandardSSLCA.pem
ln -s /usr/share/ca-certificates/gandi.net/GandiStandardSSLCA.pem /etc/ssl/certs/GandiStandardSSLCA.pem

