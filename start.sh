#!/bin/bash

ovpn_certs=./services/ovpn_server/certs
cert_certs=./services/cert_server/certs

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

if [ "$#" -ne "1" ]; then
    echo Wrong number of arguments, expected 1 argument
    exit 1
fi


prod="-f docker-compose-prod.yml"
dev=""

declare -A args
args=([prod]=$prod
      [dev]=$dev
     )

for key in "${!args[@]}"; do
    if [ "$key" = "$1" ]; then
    	echo docker-compose ${args[$key]} up -d --build
    	docker-compose ${args[$key]} up -d --build
    	docker-compose exec ovpn-server python manage.py set_env
		docker-compose exec cert-server easyrsa --batch init-pki
		docker-compose exec cert-server python manage.py build_ca
        docker-compose exec ovpn-server python manage.py create_server_cert
        docker-compose exec cert-server python manage.py set_server_crt
        exit 1
    fi
done

echo $1 dont exist, use one of the following args

for key in "${!args[@]}"; do
    echo -$key
done

exit 0
