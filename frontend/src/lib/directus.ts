import { createDirectus, rest, readItems } from '@directus/sdk';
import type { Schema } from './types';

// Récupération de l'URL publique de Directus depuis les variables d'environnement
// Fallback sur l'URL locale si absente
const directusUrl = import.meta.env.PUBLIC_DIRECTUS_URL || 'http://localhost';

// Initialisation du client Directus SDK typé avec notre Schema
export const directus = createDirectus<Schema>(directusUrl).with(rest());

/**
 * Récupère les données d'un site à partir de son slug
 */
export async function getSiteDataBySlug(slug: string) {
  try {
    const response = await directus.request(
      readItems('sites', {
        filter: {
          slug: { _eq: slug },
          actif: { _eq: true }
        }
      })
    );
    return response.length > 0 ? response[0] : null;
  } catch (error) {
    console.error(`Erreur getSiteDataBySlug pour le slug '${slug}':`, error);
    return null;
  }
}

/**
 * Récupère toutes les pages publiées associées à un ID de site
 */
export async function getPagesForSite(siteId: string) {
  try {
    return await directus.request(
      readItems('pages', {
        filter: {
          site_id: { _eq: siteId },
          statut: { _eq: 'published' }
        }
      })
    );
  } catch (error) {
    console.error(`Erreur getPagesForSite pour le site '${siteId}':`, error);
    return [];
  }
}

/**
 * Récupère les données vitrine (Hero, adresse, contact) d'un site
 */
export async function getVitrineDataForSite(siteId: string) {
  try {
    const response = await directus.request(
      readItems('vitrines', {
        filter: {
          site_id: { _eq: siteId }
        }
      })
    );
    return response.length > 0 ? response[0] : null;
  } catch (error) {
    console.error(`Erreur getVitrineDataForSite pour le site '${siteId}':`, error);
    return null;
  }
}

/**
 * Récupère tous les créateurs publiés pour l'annuaire
 */
export async function getCreatorsForAnnuaire() {
  try {
    return await directus.request(
      readItems('annuaire_createurs', {
        filter: {
          statut: { _eq: 'published' }
        },
        sort: ['-est_sponsorise', 'nom'] // Les créateurs sponsorisés apparaissent en premier
      })
    );
  } catch (error) {
    console.error('Erreur getCreatorsForAnnuaire:', error);
    return [];
  }
}

/**
 * Génère l'URL absolue d'un fichier média Directus à partir de son UUID
 */
export function getAssetUrl(fileId: string | null | undefined): string | null {
  if (!fileId) return null;
  return `${directusUrl}/assets/${fileId}`;
}
