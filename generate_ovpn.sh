url=http://localhost
certname=$1

generate_post_data()
{
    cat <<EOF
{
  "certname": "$certname"
}
EOF
}

create_req(){
    curl -X POST -H "Content-type: application/json" \
	 -H "Authorization: Bearer $SECRET_TOKEN" \
	 -H "content-type: application/json" \
	 -d "$(generate_post_data)" \
	 "$url:5002/ovpn/create_req" 2>/dev/null
}

transfer_req(){
    curl -X POST -H "Content-type: application/json" \
	 -H "Authorization: Bearer $SECRET_TOKEN" \
	 -H "content-type: application/json" \
	 -d "$(generate_post_data)" \
	 "$url:5002/ovpn/transfer_req" 2>/dev/null
}

transfer_cert(){
    curl -X POST -H "Content-type: application/json" \
	 -H "Authorization: Bearer $SECRET_TOKEN" \
	 -H "content-type: application/json" \
	 -d "$(generate_post_data)" \
	 "$url:5001/cert/transfer" 2>/dev/null
}

download_ovpn(){
   curl -X GET -H "Authorization: Bearer $SECRET_TOKEN" \
	 "$url:5002/ovpn/file/$certname.ovpn" 2>/dev/null
}

if [ "$#" -ne "1" ]; then
    echo Wrong number of arguments, expected only one
    exit 1
fi

# creating .req file
echo "Creating $certname.req file"
response=$(create_req)
status=$(echo "$response" | grep status | cut -d ',' -f1 | cut -d ':' -f2 | cut -d '"' -f2)
message=$(echo "$response" | grep message | cut -d ',' -f2 | cut -d ':' -f2 | cut -d '"' -f2)

if [ "$status" = "fail" ]; then
	echo "${message} on ovpn-server - ${status}"
	exit 1
fi

# transfering .req file to cert-server and generating .crt file
echo "transfering $certname.req file to cert-server and creating $certname.crt file"
response=$(transfer_req)
status=$(echo "$response" | grep status | cut -d ',' -f1 | cut -d ':' -f2 | cut -d '"' -f2)
message=$(echo "$response" | grep message | cut -d ',' -f2 | cut -d ':' -f2 | cut -d '"' -f2)

if [ "${status%?}" = "fail" ]; then
	echo "${message%?} on cert-server - ${status%?}"
	exit 1
fi

# transfering .crt file to ovpn-server and generating .ovpn file
echo "transfering $certname.crt file to ovpn-server and generating $certname.ovpn file"
response=$(transfer_cert)
status=$(echo "$response" | grep status | cut -d ',' -f1 | cut -d ':' -f2 | cut -d '"' -f2)
message=$(echo "$response" | grep message | cut -d ',' -f2 | cut -d ':' -f2 | cut -d '"' -f2)

if [ "$status" = "fail" ]; then
	echo "${message%?} - ${status%?}"
	exit 1
fi

echo "${message%?} - ${status%?}"

echo "Downloading $certname.ovpn..."
download_ovpn >> "$certname.ovpn"

exit 0
