#!/bin/bash


fails=""

inspect() {
	if [ $1 -ne 0 ]; then
		fails="${fails} $2"
	fi
}

# run unit and integrations tests
docker-compose up -d --build
docker-compose exec cert-server python manage.py test
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
