# fig-3.1mm-figuriniste

Cette application est codée avec le framework **Vue.js** + **Vite**.

## Pré-requis

1. Installer Node.js

2. Installer les dépendances. 
Ouvrir un terminal à la racine du projet :

```
npm install
```

## Lancement de l'application

Pour lancer l'application (équivalent à la commande ``vite``)

```
npm run app
```

L'application est alors disponible à l'adresse : http://localhost:5173/figuriniste-staging/

Cette commande sera utilisée en prod pour démarrer automatiquement l'application en local et en mode kiosque.


## Build de l'application

Pour build l'application en statique (équivalent à la commande ``vite build``)

```
npm run build
```

Le build est alors disponible dans le dossier ``/dist``.

Le fichier ``vite.config.js`` est actuellement configuré tel que la base de l'application soit ``/figuriniste-staging``, il faudra donc l'héberger dans un domaine terminant ainsi (par exemple la staging est actuellement hébergée à : https://wendygervais-reciproque.github.io/figuriniste-staging/)

Cette commande sera utilisée en staging pour générer une version de test de l'application et l'héberger sur un serveur web.