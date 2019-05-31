#!/bin/bash

info () {
    printf "\r  [ \033[00;34m..\033[0m ] $1\n"
}

prompt () {
    printf "\r  [ \033[0;33m??\033[0m ] $1\n"
}

success () {
    printf "\r\033[2K  [ \033[00;32mOK\033[0m ] $1\n"
}

fail () {
    printf "\r\033[2K  [\033[0;31mFAIL\033[0m] $1\n"
    echo ''
    exit 1
}

print_usage () {
    fail "Usage: $0 [local|localhost|raspi|pi|@IP]"
}

timestamp () {
    ts=$(date "+%Y-%m-%d %T.%3N")
    echo -e "TIMESTAMP: \033[00;34m${ts}\033[0m\n"
}

# Validation d'une adresse IP
# Proviens de https://unix.stackexchange.com/a/111846
function validate_IP () {
    local ip="$1"
    local stat=1
    if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS="$IFS"
        IFS='.'
        ip=(${ip})
        IFS="$OIFS"
        [[ "${ip[0]}" -le 255 && "${ip[1]}" -le 255 \
            && "${ip[2]}" -le 255 && "${ip[3]}" -le 255 ]]
        stat="$?"
    fi
    return "${stat}"
}

get_ip () {
    local IP="127.0.0.1"
    for i in "$@"; do
        local arg="${i}"
        #if [[ $arg =~ "(-a=*)|(--address=*)" ]]; then
        #    arg="${arg#*=}"
        #fi

        if [ "${arg}" = "local" ] || [ "${arg}" = "localhost" ] ; then
            IP="127.0.0.1"
        elif [ "${arg}" = "raspi" ] || [ "${arg}" = "pi" ]; then
            IP=$(arp -a | grep "enp3s0\|enp4s0\|eth0\|enx00e02f7000b5" | cut -d ' ' -f 2 | cut -d '(' -f 2 | cut -d ')' -f 1)
            validate_IP "${IP}"
            if [ "$?" -ne 0 ]; then
                fail "Connexion error with the raspi, @IP found: '${IP}'."
            fi
        else
            validate_IP "${arg}"
            if [ "$?" -eq 0 ]; then
                IP="${arg}"
            else
                info "Unknown argument: '$i'"
                print_usage
            fi
        fi
    done

    echo "${IP}"
}

get_port () {
    echo "5000"
}

