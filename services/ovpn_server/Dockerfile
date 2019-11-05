FROM alpine:3.7 AS builder
WORKDIR /usr/src/app
RUN apk add --no-cache openvpn && \
    apk add --no-cache openssl && \
    wget -P /usr/src/app https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz && \
    tar xvf EasyRSA-3.0.4.tgz && \
    rm EasyRSA-3.0.4.tgz
WORKDIR /usr/src/app/EasyRSA-3.0.4
RUN ./easyrsa init-pki && \
    ./easyrsa --batch gen-req server nopass && \
    cp ./pki/private/server.key /etc/openvpn/
COPY ./server.conf /etc/openvpn/
COPY ./base.conf /usr/src/app

FROM python:3.7.2-alpine
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd && \
    apk add --no-cache \
  	openssh-client \
  	ca-certificates \
  	bash && \
    apk add --no-cache openssl

WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENV EASYRSA_PATH=/usr/src/certs/EasyRSA-3.0.4
ENV REQ_PATH=/usr/certs
ENV EASYRSA_PKI=$EASYRSA_PATH/pki
ENV EASYRSA_BATCH=1

RUN ln -s $EASYRSA_PATH/openssl-easyrsa.cnf /usr/bin/openssl-easyrsa.cnf && \
    ln -s $EASYRSA_PATH/easyrsa /usr/bin/easyrsa && \
    ln -s $EASYRSA_PATH/x509-types /usr/bin/x509-types

COPY --from=builder /usr/src/app/EasyRSA-3.0.4/ /usr/src/certs/EasyRSA-3.0.4/
COPY --from=builder /etc/openvpn/ /etc/openvpn/
COPY . /usr/src/app

CMD ["/usr/src/app/entrypoint.sh"]
