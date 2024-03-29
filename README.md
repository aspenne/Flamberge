# Guide d'installation et d'utilisation - Projet Flamberge

Ce guide fournit des instructions pour configurer et exécuter l'environnement Docker pour le projet Flamberge.

## Prérequis

Assurez-vous d'avoir Docker et Docker Compose installés sur votre système.

- Docker : [Guide d'installation Docker](https://docs.docker.com/get-docker/)
- Docker Compose : [Guide d'installation Docker Compose](https://docs.docker.com/compose/install/)

## Configuration

1. Clonez ce dépôt sur votre machine locale :

   ```bash
   git clone <URL_DU_REPO> flamberge
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd flamberge
   ```

3. Modifiez les fichiers de configuration si nécessaire :

   - `FlambergeDB/init.sql` : Vous pouvez ajouter des scripts SQL d'initialisation de la base de données si besoin.
   - `FlambergeElastic/mapping.json` : Vous pouvez modifier le mapping d'index Elasticsearch si nécessaire.

## Installation

1. Lancez les conteneurs Docker en utilisant Docker Compose :

   ```bash
   docker-compose up -d
   ```

   Cela construira et lancera les conteneurs définis dans le fichier `docker-compose.yml`.

2. Vérifiez que tous les conteneurs sont en cours d'exécution :

   ```bash
   docker-compose ps
   ```

## Utilisation

- L'API est accessible à l'adresse : `http://localhost:8081`
- L'application Web est accessible à l'adresse : `http://localhost:8080`
- Elasticsearch est accessible à l'adresse : `http://localhost:9200`
- Kibana est accessible à l'adresse : `http://localhost:9201`

## Arrêt et Nettoyage

Pour arrêter les conteneurs Docker, exécutez la commande suivante :

```bash
docker-compose down
```
