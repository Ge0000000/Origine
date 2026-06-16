# AGENTS.md — Fichier de Contexte IA du Projet Origine

> ⚠️ CE FICHIER DOIT ÊTRE RÉFÉRENCÉ DANS TOUT PROMPT IA (OpenCode / Antigravity)
> Il contient toutes les règles, contraintes et décisions du projet.

---

## 🎯 Identité du Projet
- **Nom** : Micro-Agence Web Headless & Annuaire de Niche
- **Objectif** : Gérer 3 sites clients + 1 annuaire monétisé depuis un seul VPS OVH
- **Date de création** : 2026-06-16
- **Méthode de développement** : Vibecoding (OpenCode / Antigravity)

---

## 🖥️ Infrastructure Serveur
- **IP VPS** : 37.187.219.15
- **OS** : Ubuntu 26.04 LTS (codename: resolute)
- **RAM** : 3.7 Go réels + SWAP 2 Go
- **Disque** : 38 Go SSD
- **Utilisateur SSH** : ubuntu
- **CapRover Dashboard** : http://captain.37.187.219.15.nip.io (mdp: captain42)
- **CapRover version** : 1.14.2
- **Docker version** : 29.5.3

---

## 🏗️ Stack Technique (IMMUABLE — ne pas modifier sans décision explicite)

| Couche | Technologie | Contrainte |
|--------|-------------|------------|
| Orchestrateur | CapRover 1.14.2 | Docker Swarm single-node |
| CMS | Directus v11+ | SQLite UNIQUEMENT (pas PostgreSQL) |
| Frontend | Astro 5.x | SSG uniquement (pas SSR) |
| Langage | TypeScript | Strict mode, zéro `any` |
| CSS | Tailwind CSS | PurgeCSS activé |
| Hébergement | Cloudflare Pages | Free Tier |
| DNS temp. | nip.io | 37.187.219.15.nip.io |
| CI/CD | Webhook Directus → Cloudflare | Secret Token obligatoire |

---

## 🚨 Règles Absolues pour l'IA (RESPECTER IMPÉRATIVEMENT)

1. **Versions Docker ÉPINGLÉES** : Jamais de `:latest`. Toujours une version fixe. Ex: `directus/directus:11.3.5`
2. **Commentaires en français** : Tout code généré doit être commenté en français
3. **Compatibilité Ubuntu 26.04** : Privilégier les commandes éprouvées sur 24.04, tester sur 26.04
4. **RAM Directus** : Limite stricte à 300 Mo dans CapRover
5. **RAM Uptime Kuma** : Limite stricte à 128 Mo dans CapRover
6. **Sécurité API** : Permissions Directus en "Public Read-Only" pour les collections frontend
7. **Backup SQLite** : Obligatoire avant toute migration de schéma
8. **Pas de `any` TypeScript** : Le compilateur doit passer sans erreur
9. **PurgeCSS actif** : Ne jamais désactiver Tailwind PurgeCSS
10. **Test local Docker** : Toujours tester un conteneur en local avant déploiement CapRover

---

## 📦 Services & URLs

| Service | Status | URL | RAM max |
|---------|--------|-----|---------|
| CapRover | ✅ ACTIF | http://captain.37.187.219.15.nip.io | - |
| Directus CMS | ✅ ACTIF | http://directus.37.187.219.15.nip.io | 300 Mo |
| Uptime Kuma | ⏳ À déployer | http://kuma.37.187.219.15.nip.io | 128 Mo |

---

## 🔒 Ports UFW Ouverts

```
22/tcp   → SSH
80/tcp   → HTTP (CapRover nginx)
443/tcp  → HTTPS (CapRover nginx)
3000/tcp → CapRover Dashboard
```

---

## 🗂️ Structure des Sites

```
Directus (CMS central)
├── Site #1 : Matikos (Menuisier Plâtrier) → https://matikos.pages.dev
├── Site #2 : Le Croisetier (Artisan)      → À déployer
├── Site #3 : Vitrine Client C             → Cloudflare Pages
└── Site #4 : Annuaire Créateurs Cathos    → https://annuairev1catho.pages.dev
```

Chaque site est filtré par `site_id` dans Directus.

---

## 🛠️ Commandes Utiles Serveur

```bash
# État général du serveur
free -h && df -h / && sudo docker service ls

# Logs CapRover
sudo docker service logs captain-captain --tail 50

# Logs Directus (une fois déployé)
sudo docker service logs srv-captain--directus --tail 50

# Restart un service CapRover
sudo docker service update --force srv-captain--<nom-app>

# État des conteneurs
sudo docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

---

## 📅 Roadmap

| Phase | Jours | Status | Description |
|-------|-------|--------|-------------|
| Phase 0 | J1 | ✅ TERMINÉ | Setup Ubuntu, snapd, swap, CapRover, AGENTS.md |
| Phase 1 | J2-J3 | ✅ TERMINÉ | Deploy Directus SQLite, modélisation données, test API |
| Phase 2 | J4-J6 | ✅ TERMINÉ | Template Astro, connexion Directus, build local |
| Phase 3 | J7-J8 | ✅ TERMINÉ | Cloudflare Pages, webhooks, whitelist UFW |
| Phase 4 | J9-J10 | ✅ TERMINÉ | Personnalisation sites + annuaire, contenu |
| Phase 5 | J11+ | ⏳ Prochain | Monitoring, docs, lancement commercial |

---

## 📝 Historique des Décisions

- **2026-06-16** : VPS OVH acheté, Ubuntu 26.04 LTS installé
- **2026-06-16** : snapd supprimé, SWAP 2 Go créé, UFW configuré (ports 22/80/443/3000)
- **2026-06-16** : Docker 29.5.3 installé via get.docker.com
- **2026-06-16** : CapRover 1.14.2 déployé avec BY_PASS_PROXY_CHECK=TRUE
- **2026-06-16** : Domaine nip.io configuré (37.187.219.15.nip.io)
- **2026-06-16** : AGENTS.md créé (ce fichier)
- **2026-06-16** : Phase 1 terminée : Déploiement Directus 11.17.4 (SQLite), modélisation des 4 sites, rôles Public/Editor et limitation RAM à 300 Mo.
- **2026-06-16** : Phase 2 terminée : Gabarit unique Astro 5.x multi-tenant, intégration Directus SDK et Tailwind CSS, tests de compilation locale validés.
- **2026-06-16** : Phase 3 terminée : Configuration des webhooks Directus -> Cloudflare Pages.
- **2026-06-16** : Phase 4 terminée : Design Premium (Astro/Tailwind), images IA générées (Matikos, Annuaire), et injection du contenu réel via API. Mise en ligne sur https://matikos.pages.dev et https://annuairev1catho.pages.dev.
