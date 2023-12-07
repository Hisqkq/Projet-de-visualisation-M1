# 📊  Projet-de-visualisation-M1

Bienvenue sur notre projet de visualisation analytique CMI ISI.
Ce projet consiste à créer une application [Dash](https://plotly.com/dash/) en python afin de visualiser les données de l'énergie électrique [RTE](https://www.rte-france.com/) en France Métropolitaine (hors Corse).

## Cloner l'application sur votre machine

Une fois que vous avez cloné le dépot github sur votre machine, vous pouvez suivre les étapes suivantes afin d'installer toute les dépendances nécessaires pour que l'application puisse fonctionner.

Créer l'environnement virtuel:
```bash
python -m venv venv
```
Activer l'environnement virtuel (Windows):
```bash
venv\Scripts\activate
```
Activer l'environnement virtuel (Mac ou Linux):
```bash
source venv/bin/activate
```
Si il y a une erreur après avoir exécuter la commande précédente, essayez ceci:
```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
Installer les dépendances:
```bash
pip install -r requirements.txt
```
Quitter l'environnement virtuel:
```bash
deactivate
```

## ❗  Prérequis

Avant de commencer à mettre en place l'application, assurez-vous d'avoir installé MongoDB sur votre machine. MongoDB est nécessaire pour stocker et gérer les données utilisées par l'application. Suivez les instructions sur le site officiel de [MongoDB](https://www.mongodb.com/try/download/community) pour télécharger et installer la version adaptée à votre système d'exploitation.

## 💾  Initialisation de la Base de Données

Une fois MongoDB installé, vous devez initialiser la base de données et la remplir avec les données nécessaires. Pour ce faire, exécutez le script `initialize_db.py` situé dans le dossier `data` (cette étape peut durer plusieurs heures à cause des limitations des APIs...⌛):

```bash
python data/initialize_db.py
```

🚀 Une fois cette étape effectuée, tout est pret afin de lancer l'application.

Lancer l'app localement
```bash
python app.py
```


## 📃  Ressources externes

 Liste des API que nous avons utilisé pour récupérer nos données:
- Données nationales en temps réel :  https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr
- Données nationales consolidées :    https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def
- Données régionales en temps réel :  https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr
- Données régionales consolidées :    https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-cons-def


## ⭐  Contributeurs 

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/LouisDelignac">
        <img src="https://avatars.githubusercontent.com/u/102798850?v=4" width="50" height="50" alt=""/><br />
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/HamadTria">
        <img src="https://avatars.githubusercontent.com/u/102798449?v=4" width="50" height="50" alt=""/><br />
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Hisqkq">
        <img src="https://avatars.githubusercontent.com/u/120734251?v=4" width="50" height="50" alt=""/><br />
      </a>
    </td>
  </tr>
</table>
