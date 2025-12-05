---

# API Supervision

Cette API offre un ensemble d’outils pour gérer et superviser des équipements tels que des ordinateurs et des routeurs. Elle permet également d’exécuter des commandes via SSH sur ces machines. Le but est simple : offrir un point d’accès direct, efficace et sans artifice pour piloter l’infrastructure.

---

## Base URL

```
/supervision
```

---

# Gestion des Ordinateurs

## GET /Ordinateurs

Renvoie la liste complète de tous les ordinateurs enregistrés.

## GET /Ordinateur/{host_id}

Renvoie les informations d’un ordinateur spécifique.
Retourne une erreur 404 si l’équipement n’existe pas.

## POST /Ordinateur

Crée un nouvel ordinateur.
Le corps de la requête doit contenir un objet conforme au modèle `Ordinateur`.

## PUT /Ordinateur/{host_id}

Modifie un ordinateur existant.
L’opération met à jour uniquement les champs `hostname` et `ip`.

## DELETE /Ordinateur/{host_id}

Supprime un ordinateur de la base.

---

# Gestion des Routeurs

## GET /Routeurs

Renvoie la liste de tous les routeurs enregistrés.

## GET /Routeur/{host_id}

Retourne un routeur spécifique, ou une erreur 404 si non trouvé.

## POST /Routeur

Ajoute un routeur à la base de données.

## PUT /Routeur/{host_id}

Modifie un routeur existant en mettant à jour `hostname` et `ip`.

## DELETE /Routeur/{host_id}

Supprime un routeur de la base.

---

# Exécution de commandes SSH

## POST /ssh/Routeur/{id}

Exécute une commande SSH sur le routeur correspondant à l’identifiant fourni.
Retourne :

* `output` – la sortie standard de la commande
* `error` – la sortie d’erreur
* `exit_code` – le code de retour

## POST /ssh/Ordinateur/{id}

Même fonctionnement que pour les routeurs, mais sur un ordinateur.

---

# Comment utiliser l’application

1. **Lancer le serveur FastAPI**
   Démarrez votre application FastAPI via Uvicorn par exemple :

   ```
   uvicorn main:app --reload
   ```

2. **Accéder à la documentation automatique**
   Une fois le serveur en marche, la documentation Swagger est disponible à l’adresse :

   ```
   http://localhost:8000/docs
   ```

   Elle permet de tester chaque endpoint directement depuis l’interface, sans écrire une seule ligne de code client.

3. **Tester les endpoints**
   Depuis `/docs`, vous pouvez :

   * consulter les routes disponibles,
   * remplir les champs nécessaires,
   * envoyer les requêtes et observer les réponses.

4. **Utilisation via un client HTTP**
   Vous pouvez interagir avec l’API via n’importe quel outil comme `curl`, Postman, Insomnia ou depuis votre propre application Python/JS/Go, par exemple :

   ```
   curl -X GET http://localhost:8000/supervision/Ordinateurs
   ```

5. **Manipuler les équipements**

   * Ajouter ou modifier un équipement en envoyant un JSON conforme au modèle `Ordinateur` ou `Routeur`.
   * Exécuter des commandes sur une machine via les routes SSH en envoyant :

     ```json
     {
       "commandes": " <la commande que vous souhaiter executer>"
     }
     ```

L’application est simple à prendre en main : elle expose un ensemble d’outils directs, sans complexité inutile, permettant de gérer un parc informatique et d’y envoyer des commandes à distance.

Si tu veux, je peux aussi te produire une version encore plus concise, ou un modèle de README complet avec sections standardisées (installation, architecture, sécurité, roadmap, etc.).
