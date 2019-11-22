url=http://localhost
certname=$1


download_ovpn(){
   curl -X GET -H "Authorization: Bearer $SECRET_KEY" \
	 "$url:5002/ovpn/file/$certname.ovpn" 2>/dev/null
}

response=$(download_ovpn) 
status=$(echo "$response" | grep status | cut -d ',' -f1 | cut -d ':' -f2 | cut -d '"' -f2)
if [ "$status" = "fail" ]; then
	echo $response
	exit 0
fi

echo "$certname.ovpn downloaded to current folder"
echo "$response" >> "$certname.ovpn"
exit 0
