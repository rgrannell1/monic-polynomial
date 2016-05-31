#!/usr/bin/env sh




digitalOceanToken=$(cat security/digital-ocean-token)
vmConfig=$(node provision/vm-config.js)





create_response=$(curl -sS -X POST "https://api.digitalocean.com/v2/droplets" \
	-d "$vmConfig"                                      \
	-H "Authorization: Bearer $digitalOceanToken"       \
	-H "Content-Type: application/json"                 \
| jq .)

droplet_id=$(echo "$create_response" | jq .droplet.id)

if [ -z "$droplet_id" ]
then
	>&2 echo "failed to find droplet id for new VM."
	exit 1
else
	echo "created VM id = $droplet_id"
fi

sleep 30

get_response=$(curl -sS -X GET -H "Content-Type: application/json" \
	 -H "Authorization: Bearer $digitalOceanToken" \
	 "https://api.digitalocean.com/v2/droplets/$droplet_id" | jq .)

# save the created IP address as an environmental variable.

MONIC_TARGET_VM_IP="$(echo "$get_response" | jq .droplet.networks.v4[0].ip_address --raw-output)"

if [ -z "$MONIC_TARGET_VM_IP" ]
then
	>&2 echo "failed to find IP address for droplet $droplet_id"
	exit 1
else
	echo "VM ip address: $MONIC_TARGET_VM_IP"
fi

printf $MONIC_TARGET_VM_IP > security/ip_address
