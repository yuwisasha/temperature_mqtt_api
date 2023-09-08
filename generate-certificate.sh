#! /bin/bash

openssl genrsa -des3 -passout pass:x -out client.pass.key 2048
openssl rsa -passin pass:x -in client.pass.key -out client.key
rm client.pass.key
openssl req -new -key client.key -out client.csr \
    -subj "/C=UK/ST=Warwickshire/L=Leamington/O=OrgName/OU=IT Department/CN=example.com"
openssl x509 -req -days 1 -in client.csr -signkey client.key -out client.crt