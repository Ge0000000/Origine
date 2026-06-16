# Phase 3 : Déploiements Cloudflare, Webhooks et Sécurité UFW

Cette phase documente la sécurisation du serveur et la mise en place de l'intégration continue (CI/CD) entre le CMS Directus et Cloudflare Pages.

## 1. Sécurité du Serveur (UFW & Cloudflare)
Nous avons configuré le pare-feu UFW sur le VPS pour bloquer l'accès public aux ports 80 et 443, et nous avons ajouté les plages d'IP officielles de Cloudflare en liste blanche.

**Script utilisé :** `whitelist_cloudflare.sh`
- Port 22 (SSH) : Ouvert.
- Port 3000 (CapRover) : Ouvert.
- Ports 80 / 443 : Restreints aux adresses IP de Cloudflare.

*Statut : ✅ TERMINÉ*

## 2. Déploiement Frontend sur Cloudflare Pages
Les sites clients sont déployés sur Cloudflare Pages à partir du dépôt GitHub unique. Cloudflare se charge de compiler le code (Astro) pour générer les sites statiques (SSG).

### Configuration Cloudflare Pages (pour chaque site)
- **Framework :** Astro
- **Build command :** `npm install && npm run build`
- **Build output directory :** `dist`
- **Environment variables :** 
  - `DIRECTUS_URL` : http://directus.37.187.219.15.nip.io
  - `SITE_SLUG` : `matikos`, `annuaire`, etc.

*Statut : ✅ TERMINÉ*
- **Matikos** : https://matikos.pages.dev
- **Annuaire** : https://annuairev1catho.pages.dev

## 3. Webhooks Directus → Cloudflare Pages
Pour que les sites se mettent à jour automatiquement lorsque vous modifiez le contenu dans Directus, nous configurons des webhooks. Directus enverra une requête POST à Cloudflare pour déclencher un nouveau build.

### URLs des Deploy Hooks
- **Projet 1 (Matikos) :** `https://api.cloudflare.com/client/v4/pages/webhooks/deploy_hooks/6ac321d6-dcdc-4c1e-8fed-e24d01e5e72e`
- **Projet 2 (Annuaire) :** `https://api.cloudflare.com/client/v4/pages/webhooks/deploy_hooks/0fdd4f3d-e4ce-457f-9680-3415459c429c`

### Configuration dans Directus
1. Aller dans **Settings** > **Webhooks**
2. Créer un webhook :
   - **Nom :** "Build Cloudflare - Matikos"
   - **Méthode :** POST
   - **URL :** L'URL du Deploy Hook Cloudflare
   - **Statut :** Active
   - **Send Data :** Inactif (Cloudflare n'a besoin que du signal, pas des données).
   - **Triggers :**
     - Actions : `Item Created`, `Item Updated`, `Item Deleted`
     - Collections : `Sites`, `Services`, `Galerie`, `Createurs`

*Statut : ✅ EN COURS DE CONFIGURATION*

## Prochaines étapes (Phase 4)
- Personnalisation esthétique des sites et de l'annuaire.
- Ajout du contenu réel.
