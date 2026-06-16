# 📋 Phase 0 — Setup Complet du VPS OVH
**Date** : 16 Juin 2026  
**Durée** : ~1h  
**Statut** : ✅ TERMINÉ

> ⚠️ **SÉCURITÉ** : Ce fichier contient des mots de passe. Ne le partage jamais publiquement.  
> Conserve-le dans un endroit sûr (gestionnaire de mots de passe recommandé : Bitwarden, 1Password).

---

## 🔑 Récapitulatif des Accès

### 1. VPS OVH (Serveur)
| Champ | Valeur |
|-------|--------|
| **Fournisseur** | OVH |
| **Type** | VPS |
| **IP publique** | `37.187.219.15` |
| **OS** | Ubuntu 26.04 LTS (codename: resolute) |
| **Utilisateur SSH** | `ubuntu` |
| **Mot de passe SSH** | `Blackovh1` |
| **Méthode de connexion** | SSH via PuTTY ou terminal |

**Se connecter au VPS :**
```bash
# Depuis PowerShell Windows (terminal intégré)
ssh ubuntu@37.187.219.15

# Depuis PuTTY (interface graphique)
# Host Name : 37.187.219.15
# Port : 22
# Connection type : SSH
# Login : ubuntu
# Password : Blackovh1
```

---

### 2. CapRover (Orchestrateur Docker)
| Champ | Valeur |
|-------|--------|
| **URL Dashboard** | http://captain.37.187.219.15.nip.io |
| **URL alternative** | http://37.187.219.15:3000 |
| **Mot de passe** | `captain42` |
| **Version** | 1.14.2 |

**Se connecter à CapRover :**
1. Ouvrir un navigateur
2. Aller sur `http://captain.37.187.219.15.nip.io`
3. Entrer le mot de passe : `captain42`

---

## 🖥️ Caractéristiques du Serveur

| Ressource | Valeur |
|-----------|--------|
| **RAM** | 3.7 Go réels |
| **SWAP** | 2 Go (créé manuellement) |
| **Disque** | 38 Go SSD |
| **RAM utilisée au repos** | ~490 Mo |
| **Disque utilisé** | ~2.2 Go (6%) |

---

## 📋 Ce Que Nous Avons Fait (Étape par Étape)

### Étape 1 — Connexion SSH initiale
- Utilisé **PuTTY** (déjà installé sur le PC Windows)
- OVH imposait un **changement de mot de passe obligatoire** à la 1ère connexion
- Ancien mot de passe OVH : `X3Gg4Z5SmSaf` → remplacé par `Blackovh1`

---

### Étape 2 — Mise à jour du système
```bash
sudo apt-get update -y      # Rafraîchit la liste des paquets disponibles
sudo apt-get upgrade -y     # Installe toutes les mises à jour de sécurité
```
**Résultat :** Système Ubuntu 26.04 entièrement à jour.

---

### Étape 3 — Suppression de Snapd
```bash
sudo systemctl stop snapd
sudo apt-get purge snapd -y
sudo rm -rf /snap /var/snap /var/lib/snapd /root/snap ~/snap
```
**Pourquoi ?** Snapd consomme de la RAM et du CPU inutilement sur un VPS.  
**Résultat :** Snapd supprimé (il n'y avait aucun snap installé).

---

### Étape 4 — Création du fichier SWAP 2 Go
```bash
# Crée un fichier de 2 Go sur le disque
sudo fallocate -l 2G /swapfile

# Sécurise le fichier (lecture seule pour root)
sudo chmod 600 /swapfile

# Formate le fichier en espace swap
sudo mkswap /swapfile

# Active le swap immédiatement
sudo swapon /swapfile

# Rend le swap permanent (survit aux redémarrages)
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```
**Pourquoi ?** Quand la RAM est pleine, le serveur utilise le disque comme "RAM de secours".  
C'est vital pour éviter que Directus + CapRover crashent.  
**Résultat :** `Swap: 2.0Gi` confirmé avec `free -h`.

---

### Étape 5 — Configuration du Pare-feu UFW
```bash
# Politique par défaut : bloquer tout ce qui entre
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Ouvrir uniquement les ports nécessaires
sudo ufw allow 22/tcp    # SSH (connexion au serveur)
sudo ufw allow 80/tcp    # HTTP (sites web)
sudo ufw allow 443/tcp   # HTTPS (sites sécurisés)
sudo ufw allow 3000/tcp  # CapRover Dashboard

# Activer le pare-feu
sudo ufw --force enable
```
**Pourquoi ?** Protège le serveur contre les attaques extérieures.  
**Résultat :** Pare-feu actif, seuls les 4 ports utiles sont ouverts.

---

### Étape 6 — Installation de Docker
```bash
# Script officiel Docker (installe la dernière version stable)
curl -fsSL https://get.docker.com | sudo sh
```
**Pourquoi ?** CapRover et tous nos services (Directus, etc.) tournent dans des conteneurs Docker.  
**Résultat :** Docker 29.5.3 installé.

---

### Étape 7 — Installation de CapRover
```bash
# BY_PASS_PROXY_CHECK : contourne la vérification du port 80
# (nécessaire car OVH bloque la vérification automatique)
sudo docker run \
  -e ACCEPTED_TERMS=true \
  -e BY_PASS_PROXY_CHECK='TRUE' \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /captain:/captain \
  caprover/caprover
```
**Pourquoi BY_PASS_PROXY_CHECK ?** CapRover vérifie que le port 80 est accessible depuis
internet avant de s'installer. OVH bloque cette vérification au niveau réseau.  
**Résultat :** CapRover 1.14.2 déployé avec 3 services Docker actifs :

| Service Docker | Rôle |
|----------------|------|
| `captain-captain` | Le cœur de CapRover (dashboard + API) |
| `captain-nginx` | Le proxy web (reçoit les requêtes HTTP/HTTPS) |
| `captain-certbot` | Gestion automatique des certificats SSL |

---

### Étape 8 — Configuration du domaine nip.io
**Dans le dashboard CapRover** → Paramètres → Domaine racine :
```
37.187.219.15.nip.io
```
**Pourquoi nip.io ?** Service DNS gratuit qui convertit une IP en nom de domaine.  
`37.187.219.15.nip.io` pointe automatiquement vers `37.187.219.15`.  
Pas besoin d'acheter un vrai domaine pour l'instant.

**Résultat :** Les sous-domaines fonctionnent automatiquement :
- `captain.37.187.219.15.nip.io` → Dashboard CapRover
- `directus.37.187.219.15.nip.io` → Directus CMS (à déployer)
- `kuma.37.187.219.15.nip.io` → Uptime Kuma (à déployer)

---

### Étape 9 — Création de AGENTS.md
Fichier de contexte IA créé en local dans le workspace du projet.  
Sert de "mémoire" pour guider l'IA (Antigravity/OpenCode) à chaque session de code.

---

## 🐳 Services Docker Actifs

```bash
# Vérifier l'état des services (à taper dans le terminal SSH)
sudo docker service ls
```

Résultat attendu :
```
ID              NAME              MODE        REPLICAS  IMAGE
xxx             captain-captain   replicated  1/1       caprover/caprover:1.14.2
xxx             captain-certbot   replicated  1/1       caprover/certbot-sleeping:v2.11.0
xxx             captain-nginx     replicated  1/1       nginx:1.31
```

---

## 🚀 Prochaine Étape : Phase 1 — Directus

Déployer **Directus v11** (CMS headless) via CapRover avec :
- Base de données SQLite (fichier unique, pas de PostgreSQL)
- Limite RAM : 300 Mo maximum
- URL cible : `http://directus.37.187.219.15.nip.io`

---

## 🛠️ Commandes de Diagnostic Utiles

```bash
# État général du serveur
free -h && df -h / && sudo docker service ls

# Voir tous les conteneurs actifs
sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# Logs CapRover (50 dernières lignes)
sudo docker service logs captain-captain --tail 50

# Redémarrer un service CapRover
sudo docker service update --force srv-captain--<nom-de-l-app>

# Vérifier le pare-feu
sudo ufw status verbose

# Vérifier le swap
free -h
```
