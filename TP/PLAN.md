# TODO

# PARTIE 1 : TESTS UNITAIRES

Ces tests vérifie des parties de l'implémentation independamment des unes et des autres.

## 1.1 Tests de l'algorithme de triangulation

- **Trianguler 3 points** -> 1 triangle
- **Trianguler un carré** (4 points) -> 2 triangles
- **Trianguler un polygone** -> n-2 triangles
- **Moins de 3 points** -> erreur
- **Points colinéaires** -> erreur

---

## 1.2 Tests de conversion de formats binaires

- **Sérialiser un PointSet vide**
- **Sérialiser un point simple**
- **Sérialiser plusieurs points**
- **Sérialiser et déserialiser un PointSet**

## 1.3 Tests des Endpoints API

- **Requête valide** -> 200 + Triangles en binaire
- **PointSet bien crée** -> 201
- **Bad requets (format PointSetID invalide/ format binaire invalide)** -> 400
- **PointSet introuvable** -> 404
- **Erreur serveur** -> 500
- **Base de données inaccessible** -> 503

---

# PARTIE 2 : TESTS D'INTÉGRATION

Ces tests valident le comportement de l'API et les interactions entre le Triangulator et les autres services.
Ils testent les workflows complets en passant par l'interface web.

## Tests d'intégration avec PointSetManager

- **Récupération réussie** : PointSetManager retourne des données valides
- **Service indisponible** : Impossible de contacter le PointSetManager

---

# PARTIE 3 : TESTS DE PERFORMANCE

Ces tests mesurent les performances de triangulation et de conversion binaire sous différentes charges.

## 3.1 Performance de triangulation

- Ensemble de 100 points -> Mesurer le temps
- Ensemble de 1000 points -> Mesurer le temps
- Ensemble de 10000 points -> Mesurer le temps

---

## 3.2 Performance de conversion binaire

- Sérialisation : PointSet de 1000 points
- Désérialisation : Format binaire de 1000 points