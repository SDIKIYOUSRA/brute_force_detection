#!/usr/bin/zsh

# Vérifier si l'adresse IP est fournie
if [ -z "$1" ]; then
    echo "Error: No IP provided."
    exit 1
fi

IP=$1

# Ajouter une règle iptables pour bloquer l'IP
sudo iptables -A INPUT -s $IP -j DROP

# Vérification du blocage
if [ $? -eq 0 ]; then
    echo "IP $IP has been successfully blocked."
    echo "$IP $(date +%s)" >> blocked_ips.txt
else
    echo "Error blocking IP $IP."
    exit 1
fi
