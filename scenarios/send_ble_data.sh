#!/bin/bash

function showError(){
	echo -e "\e[Error : \e[0m $1"
}

UUID='6e400002-b5a3-f393-e0a9-e50e24dcca9e'

# Nb argument
if [ $# -lt 2 ]; then
	echo "Usage: $0 BD URL method. 
		BD : Bluetooth Address. You should find it using hcitool lescan.
		URL : URL si t'as pas compris.
		Actually using $#"
	exit 1
fi

# Test argument
if [[ $1 =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]; then
	data=$2
	BD=$1
	
	# Find handler	
	line=`timeout 10s gatttool -b "$BD" --characteristics |grep "$UUID"`
	handler=`echo $line|awk -F ',' '{print $3}'|awk -F '=' '{print $2}'|sed 's/ //g'`
	if [[ $handler =~ ^(0x[0-f]*)$ ]];then
		echo "Handler found"
	else
		showError "Handler not found"	
	fi
	encodedData=`echo $data|xxd -p | sed 's/0a//g'`
	echo "Data encoded"

	#echo "Sending $encodedData at $handler to $BD"
	# Sync	
	gatttool -b "$BD" --char-write-req -a "$handler" -n "$encodedData"
else
	echo "Usage: $0 BD URL. Actually using $# with a non valid BD addr"
fi
