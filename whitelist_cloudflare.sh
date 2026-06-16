#!/bin/bash
# Script de sécurisation réseau UFW (Origin Cloaking) pour le projet Origine
# Ce script limite l'accès aux ports 80 (HTTP) et 443 (HTTPS) uniquement aux adresses IP de Cloudflare.
# Le port 22 (SSH) et le port 3000 (CapRover Dashboard) restent ouverts publiquement.

echo "=========================================================="
echo "  SÉCURISATION DU VPS : WHITELIST DES IP CLOUDFLARE       "
echo "=========================================================="
echo ""

# 1. Sécurité d'administration : s'assurer que SSH et le Dashboard CapRover sont ouverts
echo "[1/5] Vérification et maintien des ports d'administration..."
sudo ufw allow 22/tcp comment 'SSH Public'
sudo ufw allow 3000/tcp comment 'CapRover Dashboard'

# 2. Supprimer les règles HTTP/HTTPS ouvertes à tout le monde
echo "[2/5] Fermeture de l'accès public direct sur les ports 80/443..."
sudo ufw delete allow 80/tcp
sudo ufw delete allow 443/tcp
sudo ufw delete allow 80
sudo ufw delete allow 443

# 3. Téléchargement des listes d'adresses IP officielles de Cloudflare
echo "[3/5] Récupération des plages d'IP Cloudflare..."
ips_v4=$(curl -s https://www.cloudflare.com/ips-v4)
ips_v6=$(curl -s https://www.cloudflare.com/ips-v6)

if [ -z "$ips_v4" ]; then
    echo "  [ERREUR] Impossible de télécharger la liste IPv4 de Cloudflare. Abandon."
    exit 1
fi

# 4. Autoriser uniquement les adresses IP Cloudflare sur les ports 80 et 443
echo "[4/5] Autorisation sélective des IPs Cloudflare..."

# Traitement des adresses IPv4
for ip in $ips_v4; do
    # On évite les doublons en ignorant si la règle existe déjà
    sudo ufw allow proto tcp from "$ip" to any port 80 comment 'Cloudflare IP' > /dev/null
    sudo ufw allow proto tcp from "$ip" to any port 443 comment 'Cloudflare IP' > /dev/null
done
echo "  - Plages d'IP IPv4 configurées."

# Traitement des adresses IPv6 (si disponibles)
if [ -n "$ips_v6" ]; then
    for ip in $ips_v6; do
        sudo ufw allow proto tcp from "$ip" to any port 80 comment 'Cloudflare IP' > /dev/null
        sudo ufw allow proto tcp from "$ip" to any port 443 comment 'Cloudflare IP' > /dev/null
    done
    echo "  - Plages d'IP IPv6 configurées."
fi

# 5. Activation et rechargement des règles du pare-feu
echo "[5/5] Rechargement du pare-feu UFW..."
sudo ufw --force enable
sudo ufw reload

echo ""
echo "=========================================================="
echo "  SÉCURISATION RÉSEAU TERMINÉE AVEC SUCCÈS !              "
echo "=========================================================="
echo ""
