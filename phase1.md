# 📋 Phase 1 — Déploiement et Configuration de Directus CMS

**Date** : 16 Juin 2026  
**Statut** : ✅ TERMINÉ

---

## 🔑 Résumé des Accès et de la Stack Directus

| Élément | Détails |
|---------|---------|
| **Image Docker** | `directus/directus:11.17.4` |
| **Bouton d'accès UI** | [http://directus.37.187.219.15.nip.io](http://directus.37.187.219.15.nip.io) |
| **Email Administrateur** | `admin@origine.dev` |
| **Mot de passe** | `Origine@Admin2026!` |
| **Base de Données** | SQLite (`/directus/database/database.sqlite`) |
| **Volume de Base de Données** | `captain--directus-database` (monté sur `/directus/database`) |
| **Volume de Médias (Uploads)**| `captain--directus-uploads` (monté sur `/directus/uploads`) |
| **Limite RAM stricte** | 300 Mo (Configurée via CapRover Service Update Override) |
| **Utilisation RAM actuelle** | ~168 Mo (stable, bien en-dessous du seuil de 300 Mo) |

---

## 🛠️ Étapes Réalisées

### 1. Déploiement de l'Application sur CapRover
- Création de l'application `directus` avec les volumes persistants dans le dashboard CapRover.
- Configuration des variables d'environnement pour utiliser **SQLite** (pas de PostgreSQL pour économiser la RAM).
- Déploiement de l'image officielle et épinglée `directus/directus:11.17.4`.
- **Résolution d'un problème d'initialisation de base de données vide :** La base SQLite avait été précédemment créée mais ne contenait aucun utilisateur administrateur. Nous avons sauvegardé la base, l'avons réinitialisée et avons forcé le redémarrage. Directus a automatiquement exécuté ses migrations internes de bootstrap et a généré le compte administrateur initial avec succès.

### 2. Application de la Limite RAM stricte (300 Mo)
Nous avons configuré une limite matérielle stricte à **300 Mo** pour le conteneur Directus via le mécanisme **Service Update Override** de CapRover. La configuration injectée dans Docker Swarm est la suivante :
```json
{
  "TaskTemplate": {
    "Resources": {
      "Limits": {
        "MemoryBytes": 314572800
      }
    }
  }
}
```
*Validation :* Le conteneur tourne actuellement à **168.3 MiB / 300 MiB**, garantissant qu'il ne saturera pas les ressources du VPS OVH (qui dispose de 3.7 Go au total).

---

## 🗄️ Modélisation des Données (Collections et Relations)

Nous avons automatisé la création des collections, des champs et des clés de relations via un script d'API. Toutes les clés primaires utilisent le format **UUID** généré par Directus.

### 1. Collection `sites`
Gère les métadonnées globales des 4 sites web.
- `id` : UUID (Clé primaire)
- `nom` : String (ex: "Matikos", "Le Croisetier")
- `slug` : String (ex: "matikos", "le-croisetier")
- `domaine` : String (ex: "matikos.fr", "lecroisetier.fr")
- `actif` : Boolean (default: `true`)

### 2. Collection `pages`
Gère le contenu textuel statique pour l'ensemble des sites.
- `id` : UUID (Clé primaire)
- `site_id` : UUID (Relation Many-to-One -> `sites.id`)
- `titre` : String
- `slug` : String
- `contenu` : Text (WYSIWYG HTML)
- `meta_description` : String (SEO)
- `statut` : String (Dropdown : `draft` / `published`)
- `date_creation` : Timestamp (Généré automatiquement à la création)

### 3. Collection `vitrines`
Contenu spécifique des vitrines B2B (Matikos / Le Croisetier).
- `id` : UUID (Clé primaire)
- `site_id` : UUID (Relation Many-to-One -> `sites.id`)
- `hero_titre` : String (Titre principal)
- `hero_description` : Text (Texte de présentation)
- `hero_image` : UUID (Relation Many-to-One -> `directus_files.id` pour l'image principale)
- `adresse` : String
- `telephone` : String
- `email` : String
- `services` : JSON (Liste de tags pour les prestations)
- `realisations` : JSON (Liste de UUIDs d'images en galerie)

### 4. Collection `annuaire_createurs`
Contenu spécifique du site de niche (Annuaire des Créateurs Catholiques).
- `id` : UUID (Clé primaire)
- `nom` : String (Nom de la marque/créateur)
- `slug` : String (ex: "atelier-saint-joseph")
- `specialite` : String (ex: "Menuiserie d'art")
- `description` : Text (WYSIWYG HTML)
- `boutique_url` : String (Lien vers leur boutique)
- `instagram_url` : String
- `logo` : UUID (Relation Many-to-One -> `directus_files.id`)
- `galerie_creations` : JSON (Liste de UUIDs d'images)
- `localisation` : String
- `est_sponsorise` : Boolean (Met en avant sur la page d'accueil)
- `statut` : String (Dropdown : `draft` / `published`)

---

## 🔒 Configuration de la Sécurité et des Rôles

### Rôle 1 : Public (API Read-Only pour Astro)
Pour permettre au framework Astro d'extraire les données sans s'authentifier lors de la phase de compilation (SSG) :
- Accès configuré en lecture seule (`read`) sur la politique Public pour les collections suivantes :
  - `sites` (filtré sur `actif = true`)
  - `pages` (filtré sur `statut = published`)
  - `vitrines` (accès total en lecture seule)
  - `annuaire_createurs` (filtré sur `statut = published`)
  - `directus_files` (permet de charger les images publiquement)

### Rôle 2 : Editor (Accès Multi-Tenant Dynamique)
Pour permettre à vos clients d'administrer leur propre site via le panel Directus sans voir ou modifier le site des autres clients :
- Création d'un champ personnalisé `site_id` (UUID) sur la table système `directus_users` avec relation vers `sites.id`.
- Création du rôle **Editor** lié à une politique **Editor Policy** (avec accès App Directus activé).
- Configuration de permissions CRUD dynamiques basées sur la variable système `$CURRENT_USER` :
  - Accès aux collections `pages` et `vitrines` restreint par la règle : `site_id == $CURRENT_USER.site_id`.
  - Autorisation complète de création et gestion des fichiers sur `directus_files` et `directus_folders` pour le téléversement des images.
  - Lecture seule autorisée sur la liste des `sites` pour la sélection initiale.

---

## 🧪 Tests d'Intégration et de Validation

Nous avons inséré des données réelles de test pour valider l'intégrité de la structure et tester la disponibilité publique des API :

```bash
# Récupérer les sites actifs (Astro)
curl -s http://localhost/items/sites -H "Host: directus.37.187.219.15.nip.io"

# Récupérer les pages publiées
curl -s http://localhost/items/pages -H "Host: directus.37.187.219.15.nip.io"

# Récupérer la vitrine de Matikos
curl -s http://localhost/items/vitrines -H "Host: directus.37.187.219.15.nip.io"

# Récupérer les créateurs de l'annuaire
curl -s http://localhost/items/annuaire_createurs -H "Host: directus.37.187.219.15.nip.io"
```

*Résultat des tests :* Les 4 requêtes retournent du JSON complet contenant les structures modélisées et les données injectées (les sites créés, la page "À propos" de Matikos, la fiche de l'artisan "Atelier Saint Joseph", etc.) sans nécessiter de jeton de sécurité, confirmant la bonne configuration de l'API publique.
