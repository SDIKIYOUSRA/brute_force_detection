#!/usr/bin/zsh

BLOCKED_IP_FILE="blocked_ips.txt"
BAN_DURATION=600
TEMP_FILE="/tmp/blocked_ips.tmp"

CURRENT_TIME=$(date +%s)

# Vérifier si le fichier existe
if [[ ! -f "$BLOCKED_IP_FILE" ]]; then
    echo "No blocked IPs to check."
    exit 0
fi
: > "$TEMP_FILE"
while read -r line; do
    IP=$(echo "$line" | awk '{print $1}')
    BLOCK_TIME=$(echo "$line" | awk '{print $2}')
    TIME_DIFF=$((CURRENT_TIME - BLOCK_TIME))

    if [[ $TIME_DIFF -ge $BAN_DURATION ]]; then
        echo "Unblocking IP: $IP"
        sudo iptables -D INPUT -s "$IP" -j DROP
    else
        echo "$line" >> "$TEMP_FILE"
    fi
done < "$BLOCKED_IP_FILE"

mv "$TEMP_FILE" "$BLOCKED_IP_FILE"
echo "Unblock process completed."
