#!/bin/bash

echo getting fingerprint ...
tls_fp=`openssl s_client -connect tuner.pandora.com:443 < /dev/null 2> /dev/null | openssl x509 -noout -fingerprint | tr -d ':' | cut -d'=' -f2`
echo got fingerprint: $tls_fp
tls_fp_key="tls_fingerprint"
tls_fp_config="${tls_fp_key} = ${tls_fp}"
config_file=$HOME/.config/pianobar/config

echo updating config ...
sed -i "s/^.*${tls_fp_key}.*$/${tls_fp_config}/" $config_file
echo config updated

echo starting pianobar
pianobar
