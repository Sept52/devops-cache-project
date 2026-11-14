#!/bin/bash
# Network policy for the cache project.
# backend: 192.168.104.1  (Ubuntu, ufw)
# proxy:   192.168.104.3  (Rocky, firewalld)
set -euo pipefail

PROXY_IP="192.168.104.3"

case "${1:-}" in
  backend)
    # ufw: deny incoming by default, allow ssh, allow API only from proxy
    apt-get update -y
    apt-get install -y ufw
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow OpenSSH
    ufw allow from "${PROXY_IP}" to any port 8080 proto tcp
    ufw --force enable
    ufw status verbose
    ;;
  proxy)
    # firewalld: public zone, open only the proxy port
    dnf install -y firewalld
    systemctl enable --now firewalld
    firewall-cmd --permanent --zone=public --add-service=ssh
    firewall-cmd --permanent --zone=public --add-port=5000/tcp
    firewall-cmd --permanent --zone=public --remove-port=6379/tcp || true
    firewall-cmd --reload
    firewall-cmd --list-all
    ;;
  *)
    echo "usage: $0 backend|proxy"
    exit 1
    ;;
esac
