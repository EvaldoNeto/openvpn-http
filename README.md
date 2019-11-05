[![Build Status](https://travis-ci.org/evaldoneto/openvpn-http.svg?branch=master)](https://travis-ci.com/evaldoneto/openvpn-http)

# openvpn-http

The main goal is to automatically start an openvpn server, generate certificates and clients through http requests.
The steps on certificates generation and server setup are based on this Digital Ocean tutorial https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-18-04 

TLS authentication will be skipped for now as my end goal does not need it

# project structure

Following the steps on the Digital Ocean tutorial, there will be two services, one responsible for only generating the certificates files, cert-server, and other responsible for the openvpn server, ovpn-server.

Inside the api folder are all scripts necessary for the service.

The project structure is based on the Michael Herman course Test-Driven Development with Python, Flask, and Docker. Here is his repo https://github.com/testdrivenio/testdriven-app-2.5

# starting the services

First be sure to have docker and docker-compose installed, that is the only thing you need.

To start just run docker-compose as follows:

```
	docker-compose up -d --build
```

To stop the services run:

```
	docker-compose down
```

So far this will start two services with a couple of endpoints, the ovpn server is not running yet.

# testing

To run the tests just run the scrip test.sh

```
	./test.sh
```

# contribute

Create a PR for an existing issue, each commit is tested on travis-ci before merge. 

Add unit tests and/or integration tests for each new method/endpoint created.

Along with the commit add the test coverage resume for the service you modified. To get the test coverage just run

```
	docker-compose exec ovpn-server python manage.py cov # for the ovnp-server service
	docker-compose exec cert-server python manage.py cov # for the cert-server service
```

# server configuration

To configure the ovpn server change the server.conf file on services/ovpn-server folder with the settings you need
Remember to update the base.conf file to match the alterations, that file will be used to create your client .ovpn file to connect to your server
