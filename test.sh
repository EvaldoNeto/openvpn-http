#!/bin/bash

ovpn_certs=./services/ovpn_server/certs
cert_certs=./services/cert_server/certs
export SECRET_KEY="TEST_TOKEN-valar_morghulis"

if [ -d "$ovpn_certs" ]; then
    echo "$ovpn_certs exist"
else
	echo "creating $ovpn_certs"
	`mkdir $ovpn_certs`
fi

if [ -d "$cert_certs" ]; then
    echo "$cert_certs exist"
else
	echo "creating $cert_certs"
	`mkdir $cert_certs`
fi

fails=""

inspect() {
	if [ $1 -ne 0 ]; then
		fails="${fails} $2"
	fi
}

# run unit and integrations tests
export SECRET_KEY="my_precious"
docker-compose up -d --build
docker-compose exec ovpn-server python manage.py set_env
docker-compose exec cert-server easyrsa --batch init-pki
docker-compose exec cert-server python manage.py build_ca
docker-compose exec ovpn-server python manage.py create_server_cert
docker-compose exec cert-server python manage.py set_server_crt
inspect $? cert_server
docker-compose exec cert-server flake8 project
inspect $? cert-server-lint
docker-compose exec ovpn-server python manage.py test
inspect $? ovpn_server
docker-compose exec ovpn-server flake8 project
inspect $? ovpn-server-lint
docker-compose down

# return proper code
if [ -n "${fails}" ]; then
	echo "Tests failed: ${fails}"
	exit 1
else
	echo "Tests passed!"
	exit 0
fi
