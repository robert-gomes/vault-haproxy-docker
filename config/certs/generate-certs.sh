#!/usr/bin/env bash

cleanup(){
    rm -rf vault-root-ca.*
}

# generate ca
openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout vault-root-ca.key -out vault-root-ca.pem -subj "/CN=localhost"
openssl x509 -outform pem -in vault-root-ca.pem -out vault-root-ca.crt

openssl req -new -nodes -newkey rsa:2048 -keyout vault.key -out vault.csr -subj "/CN=localhost"
openssl x509 -req -sha256 -days 1024 -in vault.csr -CA vault-root-ca.pem -CAkey vault-root-ca.key -CAcreateserial -extfile domains -out vault.crt

cat vault.crt vault.key >> vault.pem