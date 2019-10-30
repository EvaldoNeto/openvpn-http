FROM alpine:3.7
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
