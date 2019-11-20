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

if [ "$#" -ne "2" ]; then
    echo Wrong number of arguments, expected 2 argument
    exit 1
fi


prod="-f docker-compose-prod.yml"
dev=""

declare -A args
args=([prod]=$prod
      [dev]=$dev
     )


if [ "$2" = "start" ]; then
    echo "starting the services..."
elif [ "$2" = "rebuild" ]; then
    ask_question=true
    while [ "$ask_question" = "true" ]
    do
        echo "rebulding all services, all current certificates will be erased, are you sure you want to proceed? (yes/no)"
        read are_you_sure
        if [ "$are_you_sure" = "yes" ]; then
            echo "removing all current certificates from both services"
            docker-compose exec ovpn-server python manage.py flush_certs
            docker-compose exec cert-server python manage.py flush_certs
            ask_question="false"
        elif [ "$are_you_sure" = "no" ]; then
            echo "exiting the build"
            exit 0
        else
            echo "wrong argument, please enter yes or no"
        fi
    done
else
    echo "Wrong second argument, use start or rebuild"
    exit 1
fi

for key in "${!args[@]}"; do
    if [ "$key" = "$1" ]; then
    	echo docker-compose ${args[$key]} up -d --build
    	docker-compose ${args[$key]} up -d --build
    	docker-compose exec ovpn-server python manage.py set_env
		docker-compose exec cert-server python manage.py set_env
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
