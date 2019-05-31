#!/bin/bash
home="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${home}/scenarios/utils.sh"

IP=$(get_ip "$@")
port=$(get_port)
if [ $? -ne 0 ]; then
    fail "Impossible to parse the IP address."
fi

info "IP is ${IP}"
timestamp

curl -X GET http://${IP}:${port}/is_open
timestamp
