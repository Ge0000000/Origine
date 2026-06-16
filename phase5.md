# Phase 5 : Monitoring et Finalisation

**Date :** 16 Juin 2026
**Statut :** ✅ TERMINÉE

## 1. Déploiement d'Uptime Kuma
Afin de garantir la disponibilité continue des sites web et de l'API Directus, nous avons déployé un outil de surveillance autonome sur le serveur.

- **Nom de l'application :** `kuma`
- **Version Docker :** `louislam/uptime-kuma:1.23.13` (version fixe selon nos règles strictes).
- **RAM Limite :** Strictement limitée à 128 MB dans CapRover pour éviter toute fuite de mémoire.
- **Port d'écoute :** `3001`
- **Connexion Sécurisée :** Force SSL (HTTPS) activé via Let's Encrypt / CapRover.
- **URL d'accès :** https://kuma.37.187.219.15.nip.io

## 2. Configuration (À faire par l'administrateur)
Pour finaliser l'installation, vous devez vous connecter à l'interface d'Uptime Kuma et configurer les moniteurs.

### A. Première connexion
1. Rendez-vous sur https://kuma.37.187.219.15.nip.io
2. Créez votre compte administrateur (identifiant et mot de passe de votre choix).

### B. Ajout des Moniteurs
Dans le tableau de bord Uptime Kuma, cliquez sur **Ajouter un moniteur** et créez 3 moniteurs de type "HTTP(s)" :

1. **Directus CMS API**
   - URL : `http://directus.37.187.219.15.nip.io/server/health` (Le endpoint /server/health est très rapide et parfait pour vérifier si la base SQLite répond).
   - Intervalle de vérification : 60 secondes.

2. **Site Matikos**
   - URL : `https://matikos.pages.dev`
   - Intervalle : 60 secondes.

3. **Site Annuaire**
   - URL : `https://annuairev1catho.pages.dev`
   - Intervalle : 60 secondes.

### C. Alertes (Optionnel)
Vous pouvez configurer des alertes dans la section **Paramètres > Notifications** (par email via SMTP, Discord, Slack, ou Telegram) pour être prévenu en temps réel si un service devient indisponible.

## Conclusion du Projet "Origine"
Le projet "Micro-Agence Web Headless" est officiellement terminé et en production. 
L'infrastructure (CapRover, Directus), le développement Frontend (Astro, Tailwind), l'intégration continue (Cloudflare Pages, Webhooks) et le monitoring (Uptime Kuma) sont 100% fonctionnels et documentés.
