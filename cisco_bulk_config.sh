#!/bin/bash

####################################
# USER VARIABLES
####################################

PROTOCOL="ssh"              # ssh or telnet
USERNAME="aldrees"
PASSWORD='Aldree$$ruh011'

START_IP=1
END_IP=14

IP_PREFIX="192.168.10"

LOGFILE="cisco_bulk_$(date +%Y%m%d_%H%M%S).log"

####################################
# CISCO COMMANDS
####################################

read -r -d '' CONFIG_CMDS << 'EOF'
conf t

vlan 16
 name Wifi-B2

vlan 17
 name Wifi-B3

end

wr
EOF

####################################
# REVIEW COMMANDS
####################################

read -r -d '' VERIFY_CMDS << 'EOF'
show vlan brief | include 16|17
show ip interface brief
show running-config | include default-gateway
EOF

####################################
# PROCESS
####################################

for OCTET in $(seq $START_IP $END_IP)
do

    IP="${IP_PREFIX}.${OCTET}"

    echo ""
    echo "======================================="
    echo "Processing $IP"
    echo "======================================="

    echo "===== $IP =====" | tee -a "$LOGFILE"

    if [ "$PROTOCOL" = "ssh" ]; then

        ssh "$USERNAME@$IP" << EOF | tee -a "$LOGFILE"

terminal length 0

$CONFIG_CMDS

$VERIFY_CMDS

exit

EOF

    else

        expect << EOF | tee -a "$LOGFILE"

set timeout 30

spawn telnet $IP

expect "Username:"
send "$USERNAME\r"

expect "Password:"
send "$PASSWORD\r"

expect "#"

send "terminal length 0\r"

send "$CONFIG_CMDS\r"

send "$VERIFY_CMDS\r"

send "exit\r"

expect eof

EOF

    fi

done

echo ""
echo "======================================="
echo "Completed"
echo "Log File: $LOGFILE"
echo "======================================="
