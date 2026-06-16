# 📋 Phase 2 — Gabarit Astro & Connexion Directus

**Date** : 16 Juin 2026  
**Statut** : ✅ TERMINÉ

---

## 🏗️ Architecture du Gabarit Unique (Multi-Tenant)

Afin d'optimiser la maintenance et les ressources du VPS, nous avons développé une architecture à **gabarit unique dynamique**. Les différents sites clients sont compilés de manière autonome à partir de la même base de code grâce à la variable d'environnement `SITE_SLUG`.

```
                  ┌──────────────────────┐
                  │   Code Source Astro  │
                  └──────────┬───────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
   SITE_SLUG=matikos  SITE_SLUG=annuaire-...  SITE_SLUG=le-croisetier
            │                │                │
            ▼                ▼                ▼
     [Dossier dist/]   [Dossier dist/]   [Dossier dist/]
       (Vitrine B2B)     (Annuaire B2C)    (Vitrine B2B)
```

---

## 🗂️ Organisation des Dossiers du Projet

Le projet Astro a été initialisé dans le sous-dossier `frontend/` du workspace :
```
frontend/
├── src/
│   ├── layouts/
│   │   └── Layout.astro         # Shell HTML global, thèmes et polices dynamiques
│   ├── components/
│   │   ├── Navbar.astro         # Header adaptatif (liens et design selon site)
│   │   ├── Footer.astro         # Footer adaptatif avec contacts de la vitrine
│   │   ├── Hero.astro           # Section Hero avec image de fond Directus
│   │   ├── Services.astro       # Liste des expertises (Vitrines)
│   │   ├── Gallery.astro        # Galerie photos avec fallback Unsplash (Vitrines)
│   │   ├── ContactForm.astro    # Formulaire de contact glassmorphism
│   │   └── CreatorCard.astro    # Fiche synthétique d'un créateur (Annuaire)
│   ├── lib/
│   │   ├── types.ts             # Typage strict (interfaces) du schéma Directus
│   │   └── directus.ts          # Initialisation du client SDK Directus & requêtes
│   ├── pages/
│   │   ├── index.astro          # Landing page adaptative (Vitrine vs Annuaire)
│   │   ├── [...slug].astro      # Routage dynamique des sous-pages CMS (SSG)
│   │   └── createurs/
│   │       └── [slug].astro     # Fiches détaillées des créateurs (Annuaire)
│   └── styles/
│       └── global.css           # Directives Tailwind et micro-animations
├── astro.config.mjs             # Config Astro (mode static, integration Tailwind)
├── tailwind.config.mjs          # Configuration des sources de scan Tailwind
└── package.json                 # Dépendances (Astro 5.x, SDK, Tailwind)
```

---

## 🔑 Connexion Directus & Typage Strict (TypeScript)

Conformément à la règle de **zéro `any` en mode TypeScript strict** :
- Le fichier `src/lib/types.ts` déclare les types exacts pour `Site`, `Page`, `Vitrine` et `Createur`.
- Le client SDK est initialisé en injectant ces types via `createDirectus<Schema>(url).with(rest())`.
- Le chargement des médias (images) est géré de manière robuste en convertissant les UUIDs de Directus en URLs d'images absolues via la fonction `getAssetUrl(uuid)`.

---

## 🎨 Conception Visuelle & Thèmes (Tailwind CSS)

Le gabarit dispose d'un design moderne, haut de gamme et dynamique :
- **Glassmorphism** : Cartes et en-têtes translucides avec flou d'arrière-plan (`backdrop-blur-md bg-white/80`).
- **Aesthetics harmonieuses** : Utilisation de dégradés et de palettes de couleurs adaptées selon le site :
  - **Matikos** : Tons forêt/vert émeraude (`from-emerald-600 to-teal-700`). Polices : Outfit.
  - **Annuaire Catholique** : Tons or/ambre chaleureux (`from-amber-600 to-yellow-700`). Polices : Outfit.
- **Polices Premium** : Chargement de Google Fonts (Outfit pour les vitrines et l'annuaire, Inter pour la lisibilité).
- **Micro-animations** : Effets de soulèvement (`hover-lift`) sur les boutons et les fiches créateurs pour dynamiser l'interface.

---

## 🧪 Tests de Compilation Locale (SSG)

Nous avons validé la génération statique locale pour les deux principaux cas de figure en connectant le build à l'API Directus sur le VPS.

### 1. Test de compilation : Vitrine B2B (Matikos)
```bash
# Lancement de la compilation
$env:SITE_SLUG="matikos"; $env:PUBLIC_DIRECTUS_URL="http://directus.37.187.219.15.nip.io"; npm run build
```
*Résultat :* Compilation réussie en **1.84s**.
- Génération de `/index.html` (Landing page avec Hero, Services, Galerie et formulaire de contact).
- Génération de `/a-propos/index.html` (Page secondaire récupérant le WYSIWYG de Directus).
- Aucune page de créateur générée (correct pour ce site).

### 2. Test de compilation : Annuaire des Créateurs
```bash
# Lancement de la compilation
$env:SITE_SLUG="annuaire-createurs-catholiques"; $env:PUBLIC_DIRECTUS_URL="http://directus.37.187.219.15.nip.io"; npm run build
```
*Résultat :* Compilation réussie en **2.14s**.
- Génération de `/index.html` (Moteur de recherche et grille des créateurs catholiques).
- Génération de `/createurs/atelier-saint-joseph/index.html` (Fiche de détail avec bio liturgique et liens de boutique).
- Aucune page secondaire générée (correct car aucune sous-page n'est liée à l'annuaire).
