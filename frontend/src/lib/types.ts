// Interfaces TypeScript correspondant à notre schéma Directus

export interface Site {
  id: string; // UUID
  nom: string;
  slug: string;
  domaine: string;
  actif: boolean;
}

export interface Page {
  id: string; // UUID
  site_id: string; // UUID de relation vers Site
  titre: string;
  slug: string;
  contenu: string; // HTML WYSIWYG
  meta_description: string;
  statut: 'draft' | 'published';
  date_creation: string; // ISO Timestamp
}

export interface Vitrine {
  id: string; // UUID
  site_id: string; // UUID
  hero_titre: string;
  hero_description: string;
  hero_image: string | null; // UUID du fichier Directus
  adresse: string;
  telephone: string;
  email: string;
  services: string[]; // Liste de tags stockée sous forme de tableau JSON
  realisations: string[]; // Liste d'UUIDs d'images en galerie stockée en JSON
}

export interface Createur {
  id: string; // UUID
  nom: string;
  slug: string;
  specialite: string;
  description: string; // HTML WYSIWYG
  boutique_url: string;
  instagram_url: string;
  logo: string | null; // UUID du fichier
  galerie_creations: string[] | null; // Liste d'UUIDs d'images en JSON
  localisation: string;
  est_sponsorise: boolean;
  statut: 'draft' | 'published';
}

// Schéma Directus complet pour typage strict du client SDK
export interface Schema {
  sites: Site[];
  pages: Page[];
  vitrines: Vitrine[];
  annuaire_createurs: Createur[];
}
