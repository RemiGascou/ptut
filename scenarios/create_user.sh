#!/bin/bash
home="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${home}/scenarios/utils.sh"

IP=$(get_ip "$@")
port=$(get_port)
if [ $? -ne 0 ]; then
    fail "Impossible to parse the IP address."
fi

info "IP is ${IP}"

token=`curl -X POST -H "Content-Type: application/json" -d '{"username":"pi","password":"pwd"}' http://${IP}:${port}/auth  2>/dev/null | jq -r ".access_token"`

curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT ${token}" -d '{"new_user":"celia","password":"chat"}' http://${IP}:${port}/register
