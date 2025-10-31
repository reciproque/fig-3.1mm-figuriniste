# fig-3.1mm-figuriniste

Cette application est codée avec le framework **Vue.js** + **Vite**.

## Pré-requis

1. Installer Node.js

2. Installer les dépendances. 
Ouvrir un terminal à la racine du projet :

```
npm install
```

## Lancement local de l'application

Pour lancer l'application (équivalent à la commande ``vite``)

```
npm run app
```

L'application est alors disponible à l'adresse : http://localhost:5173//figuriniste/

Le chemin ```/figuriniste/``` est renseigné dans le fichier ``vite.config.js`` :

```
  base: '/figuriniste/',
```

Cette commande sera utilisée en prod pour démarrer automatiquement l'application en local et en mode kiosque.

## Lancement automatique

TODO // Démarrage automatique avec .bat + planificateur de tâches Windows + mode kiosque

## Build et hébergement en ligne de l'application

Pour build l'application en statique (équivalent à la commande ``vite build``)

```
npm run build
```

Le build est alors disponible dans le dossier ``/dist``.

Cette commande sera utilisée en staging pour générer une version de test de l'application et l'héberger sur un serveur web. Par exemple,


- La **DEV** est hébergée à http://www.fig.reciproque.com/figuriniste-dev/ ; dans le fichier ``vite.config.js`` :

```
  base: '/figuriniste-dev/',
```

- La **STAGING** est hébergée à : http://www.fig.reciproque.com/figuriniste-staging/ ; dans le fichier ``vite.config.js`` :

```
  base: '/figuriniste-staging/',
```


Ajouter à la racine :

- un fichier ``.htaccess`` afin de masquer les index et protéger le site par mot de passe :
  
```
Options -Indexes

AuthType Basic
AuthName "Espace protégé"
AuthUserFile /home/reciproqv-wge/figurine/figuriniste-staging/.htpasswd
Require valid-user
```

- un fichier ``.htpasswd``, à générer en utilisant la commande : ``htpasswd -c /path/.htpasswd nom_utilisateur``
  
```
nom_utilisateur:mot_de_passe_encrypté
```

  
- un fichier ``robots.txt`` pour éviter l'indexation du site :

```
User-agent: *
Disallow: /
```

## Données

Les dialogues et textes d'interface sont respectivement issus des fichiers ``dialogs.json`` et ``interface.json``.
Ceux-si sont fetch depuis le dossier public, il est donc possible de les remplacer à la volée sans relancer l'application locale ou sans re-build les fichiers statiques.

## Interfaçage Phidget

TODO

