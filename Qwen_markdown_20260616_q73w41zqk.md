# 📄 PRD : Micro-Agence Web Headless & Annuaire Niche

**Version :** 1.0  
**Date :** 17 Juin 2026  
**Stack Cible :** Ubuntu 26.04 LTS + CapRover + Directus (SQLite) + Astro + Cloudflare Pages  
**Méthode de Développement :** Vibecoding (OpenCode / Anomaly)

---

## 1. 🎯 Résumé Exécutif (Executive Summary)
Ce projet vise à déployer une infrastructure web "Headless" ultra-économique sur un VPS OVH ancien (2017, 2 Go RAM). L'objectif est double :
1. **B2B :** Fournir une plateforme CMS (Directus) permettant de gérer et déployer 3 sites vitrines clients via Astro/Cloudflare Pages.
2. **B2C / Revenu Passif :** Opérer un 4ème site (Annuaire de Niche) générant des revenus d'affiliation et de sponsoring pour autofinancer l'infrastructure.

Le développement sera assisté par IA (Vibecoding), nécessitant une architecture rigoureuse, sécurisée et optimisée pour compenser les limites matérielles et le risque d'hallucination de l'IA sur Ubuntu 26.04.

---

## 2. 👥 Personas & Cas d'Usage

| Persona | Besoins Critiques | Solution Technique |
| :--- | :--- | :--- |
| **L'Admin (Vous)** | Gérer 4 sites depuis un seul endroit, monitoring serveur, maintenance rapide via IA. | Directus Admin UI, CapRover Dashboard, Uptime Kuma, OpenCode. |
| **Le Client (Non-tech)** | Modifier textes/images depuis mobile sans casser le site, validation immédiate. | Directus App Mobile-Friendly, Webhook Auto-Rebuild Cloudflare. |
| **Le Visiteur Final** | Site ultra-rapide (<1s), accessible en 3G/4G, SEO optimisé. | Astro SSG, Cloudflare Edge Network, TypeScript Strict. |
| **Le Sponsor (Annuaire)** | Visibilité maximale, backlink dofollow, statistiques de clics. | Mise en avant programmatique dans Directus, liens trackés. |

---

## 3. 🏗️ Architecture Technique & Contraintes

### 3.1 Infrastructure Backend (VPS OVH)
- **OS :** Ubuntu 26.04 LTS (Snapd désinstallé obligatoirement).
- **Orchestrateur :** CapRover (Docker Swarm mode single-node).
- **CMS :** Directus v11+ en mode **SQLite** (Fichier unique, pas de PostgreSQL).
- **Ressources Max :** Swap 2Go obligatoire. RAM Directus ≤ 300Mo. RAM Presearch ≤ 128Mo.
- **Sécurité Réseau :** Whitelist stricte des IP Cloudflare sur UFW. Pas de nœud VPN/Mysterium.

### 3.2 Frontend & Déploiement
- **Framework :** Astro 5.x (Mode Static Site Generation uniquement).
- **Langage :** TypeScript (Strict mode, zéro `any`).
- **Style :** Tailwind CSS (PurgeCSS activé par défaut).
- **Hébergement :** Cloudflare Pages (Free Tier).
- **CI/CD :** Webhook Directus → Cloudflare Build Hook (avec Secret Token).

### 3.3 Règles de Vibecoding (Spécifiques OpenCode)
- **Contexte Obligatoire :** Tout prompt doit référencer le fichier `AGENTS.md`.
- **Versions Docker :** Toujours épinglées (ex: `directus/directus:11.3.5`). Jamais de `:latest`.
- **Compatibilité OS :** Privilégier les commandes éprouvées sur 24.04. Tester ligne par ligne sur 26.04.
- **Documentation :** Commentaires pédagogiques en français exigés dans tout code généré.
- **Sécurité API :** Permissions Directus en "Public Read-Only" pour les collections frontend.

---

## 4. 📦 Livrables Fonctionnels

### 4.1 Le Backend CMS (Directus)
- [ ] Schéma de données unifié pour 4 sites (Collections séparées ou filtrées par `site_id`).
- [ ] Rôles utilisateurs : Admin (vous), Éditeur (client), Public (API read-only).
- [ ] Configuration Webhook native vers Cloudflare.
- [ ] Backup automatique nightly du fichier SQLite vers stockage externe (S3/B2).

### 4.2 Le Template Astro (Monorepo ou Dossier Unique)
- [ ] Structure réutilisable pour les 3 sites clients + 1 annuaire.
- [ ] Client SDK Directus typé avec gestion du cache et fallback offline.
- [ ] Composants UI atomiques (Hero, Features, Testimonials, Listing, Detail).
- [ ] Scripts de build/déploiement Wrangler CLI sécurisés.

### 4.3 L'Annuaire de Niche (Site #4)
- [ ] Page de listing avec filtres dynamiques (catégorie, tag, localisation).
- [ ] Page détail optimisée SEO (Schema.org JSON-LD inclus).
- [ ] Emplacements réservés pour liens d'affiliation et badges "Sponsor".
- [ ] Formulaire de soumission/sponsoring connecté à Directus.

### 4.4 Monitoring & Maintenance
- [ ] Uptime Kuma installé via CapRover (alertes Discord/Email).
- [ ] Logs Docker centralisés et rotatifs (pour ne pas saturer le disque).
- [ ] Script de diagnostic système compatible Ubuntu 26.04.

---

## 5. ⚠️ Gestion des Risques

| Risque | Probabilité | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| OOM Killer (RAM) | Haute | Critique | Swap 2Go + Limites CapRover strictes + SQLite. |
| Hallucination IA (26.04) | Moyenne | Élevé | Fichier AGENTS.md + Test local Docker avant déploiement. |
| Blocage Webhook CF | Moyenne | Moyen | Whitelist UFW IP Cloudflare + Secret Token. |
| Corruption SQLite | Faible | Critique | Backup externe automatisé + Volume Docker persistant. |
| Dépassement Free Tier CF | Faible | Moyen | Debounce webhook + Cache agressif API Directus. |

---

## 6. 📈 Métriques de Succès (KPIs)

- **Performance :** Lighthouse Score > 95 (Mobile & Desktop) sur les 4 sites.
- **Stabilité :** Uptime > 99.9% sur 30 jours (hors maintenance planifiée).
- **Business :** Annuaire génère ≥ 4€/mois (remboursement VPS) dans les 60 jours post-lancement.
- **Efficacité Dev :** Temps moyen de modification client < 5 min (de la demande au live).
- **Ressources :** Consommation RAM VPS stable < 1.6 Go en charge normale.

---

## 7. 🗺️ Roadmap de Développement (Vibecoding)

1. **Phase 0 (J1) :** Setup Ubuntu 26.04, purge snapd, swap, install CapRover, création `AGENTS.md`.
2. **Phase 1 (J2-J3) :** Deploy Directus SQLite, modélisation données, test API locale.
3. **Phase 2 (J4-J6) :** Création Template Astro, connexion Directus, test build local.
4. **Phase 3 (J7-J8) :** Déploiement Cloudflare Pages, config webhooks, whitelist UFW.
5. **Phase 4 (J9-J10) :** Personnalisation Sites Clients + Annuaire, remplissage contenu.
6. **Phase 5 (J11+) :** Monitoring, documentation revente (Starter Kit), lancement commercial.