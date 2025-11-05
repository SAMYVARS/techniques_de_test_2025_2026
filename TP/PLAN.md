# TODO

# PARTIE 1 : TESTS UNITAIRES

Ces tests vérifie des parties de l'implémentation independamment des unes et des autres.

## 1.1 Tests de l'algorithme de triangulation

### Objectif : Vérifier que l'algorithme de triangulation fonctionne correctement pour divers ensembles de points

- **Trianguler 3 points** -> Vérifier qu'un triangle est formé
- **Trianguler un carré** (4 points) -> Vérifier que 2 triangles sont formés, couvrant tout le carré, sans chevauchement
- **Trianguler un polygone** -> Tester plusieurs configurations (pentagone, hexagone, etc.), vérifier que la triangulation est correcte, sans chevauchement et couvre toute la surface. Vérifier également que pour N points on obtient bien N-2 triangles
- **Moins de 3 points** -> S'assurer qu'aucun triangle n'est formé
- **Points colinéaires** -> S'assurer qu'aucun triangle n'est formé

## 1.2 Tests de conversion de formats binaires

### Objectif : Vérifier que la conversion entre les formats PointSet et binaire fonctionne correctement.

**Sérialisation** : Transformer un PointSet en une séquence d'octets pour un traitement plus rapide
**Désérialisation** : Reconstruire un PointSet à partir d'une séquence d'octets

**Format binaire utilisé** : 
- En-tête : 4 octets (nombre de points)
- Chaque point : 8 octets (4 octets pour la coordonnée x + 4 octets pour la coordonnée y en float)

- **Sérialiser un PointSet vide** -> Vérifier que la serialisation produit uniquement l'en-tête avec 0 points (4 octets)
  - Exemple : `PointSet([])` -> `b'\x00\x00\x00\x00'` (4 octets)
- **Sérialiser un point simple** -> Vérifier que la serialisation produit l'en-tête + 8 octets pour les coordonnées x,y du point. 12 octets au total
  - Exemple : `PointSet([(1.0, 2.0)])` -> 12 octets (4 en-tête + 4 pour x + 4 pour y)
- **Sérialiser plusieurs points** -> Vérifier que la serialisation produit l'en-tête + 8 octets par point et que la taille totale augmente linéairement en fonction du nombre de points
  - Exemple : `PointSet([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])` → 28 octets (4 en-tête + 3×8)
- **Sérialiser et déserialiser un PointSet** -> Vérifier qu'un PointSet sérialisé puis désérialisé conserve le même nombre de points et les mêmes valeurs

## 1.3 Tests des Endpoints API

### Objectif : Vérifier que les endpoints de l'API fonctionnent correctement et gèrent les erreurs

- **Requête valide** -> retour 200 + mock du triangulator + vérification de la réponse
- **PointSet bien crée** -> retour 201 + ID + mock du PointSetManager
- **Bad requets (format PointSetID invalide/ format binaire invalide)** -> Envoyer des données malformées et vérifier que le serveur retourne 400
- **PointSet introuvable** -> Mock du PointSetManager pour retourner une erreur 404 not found
- **Erreur serveur** -> Mock du Triangulator pour lever RuntimeError + erreur 500
- **Base de données inaccessible** -> Mock du PointSetManager pour lever ConnectionError + erreur 503

---

# PARTIE 2 : TESTS D'INTÉGRATION

Ces tests valident le comportement de l'API et les interactions entre le Triangulator et les autres services.
Ils testent les workflows complets en passant par l'interface web.

## Tests d'intégration avec PointSetManager et Triangulator

### Objectif : Vérifier que l'API interagit correctement avec le PointSetManager et le Triangulator

- **Récupération réussie** : PointSetManager retourne des données valides
- **Service indisponible** : Impossible de contacter le PointSetManager
- **Vérifier un enchaînement complet** : "Upload PointSet -> Trianguler -> Récupérer résultats" -> Vérifier que chaque étape fonctionne correctement et que les données sont cohérentes à chaque étape

---

# PARTIE 3 : TESTS DE PERFORMANCE

Ces tests mesurent les performances de triangulation et de conversion binaire sous différentes charges.

## 3.1 Performance de triangulation

### Objectif : Mesurer le temps de triangulation pour différents ensembles de points

- Ensemble de 100 points -> Mesurer le temps moyen sur un certains nombre d'itérations
- Ensemble de 1000 points -> Mesurer le temps moyen sur un certains nombre d'itérations
- Ensemble de 10000 points -> Mesurer le temps moyen sur un certains nombre d'itérations

## 3.2 Performance de conversion binaire

### Objectif : Mesurer le temps de sérialisation et désérialisation pour différents ensembles de points

- Sérialisation : PointSet de 1000 points -> Mesurer le temps moyen sur un certains nombre d'itérations
- Désérialisation : Format binaire de 1000 points -> Mesurer le temps moyen sur un certains nombre d'itérations

## 3.3 Test de consommation mémoire

### Objectif : Mesurer la consommation mémoire lors de la triangulation et de la conversion binaire

- **Triangulation de 10000 points** -> Mesurer le pic mémoire utilisé -> utiliser `tracemalloc`
- **Sérialisation de 10000 points** -> Comparer la taille en mémoire (PointSet vs binaire)
- **Triangulations successives** -> Exécuter 100 triangulations consécutives -> vérifier qu'il n'y a pas de fuite mémoire (mémoire finale ≈ mémoire initiale)
- **Format binaire vs PointSet** -> Mesurer le gain mémoire du format binaire par rapport à l'objet Python