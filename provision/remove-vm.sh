#!/usr/bin/env sh




digitalOceanToken=$(cat security/digital-ocean-token)

droplet_id=$(cat security/droplet_id)




curl -sS -X DELETE "https://api.digitalocean.com/v2/droplets/$droplet_id" \
	-H "Authorization: Bearer $digitalOceanToken"       \
