#!/bin/bash
# Creates a gateway to forward traffic to arietta

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -o usb0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i usb0 -o wlan0 -j ACCEPT