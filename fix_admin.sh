#!/bin/bash
# Test de connexion admin Directus via le proxy CapRover
# Projet Origine - Phase 1

echo "=== TEST CONNEXION ADMIN DIRECTUS ==="
echo ""

# Test 1 : Login via proxy CapRover (port 80, Host header)
echo "--- Test login API via proxy (dev) ---"
curl -s -X POST http://localhost/auth/login \
  -H "Host: directus.37.187.219.15.nip.io" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@origine.dev","password":"Origine@Admin2026!"}' \
  | cut -c1-300

echo ""
echo "--- Test login API via proxy (local) ---"
curl -s -X POST http://localhost/auth/login \
  -H "Host: directus.37.187.219.15.nip.io" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@origine.local","password":"Origine@Admin2026!"}' \
  | cut -c1-300

echo ""
echo ""

# Test 2 : Vérifier que la DB a bien été réinitialisée
echo "--- Taille de la base SQLite actuelle ---"
sudo ls -lh /var/lib/docker/volumes/captain--directus-database/_data/

echo ""
echo "--- Fichiers de backup ---"
sudo ls -la /var/lib/docker/volumes/captain--directus-database/_data/*.bak.* 2>/dev/null || echo "Aucun backup trouvé (base jamais supprimée ou déjà propre)"

echo ""
echo "=== FIN TEST ==="
