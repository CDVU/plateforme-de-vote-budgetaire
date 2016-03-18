# Installation du projet

## Configuration de l'environnement

 1 - Installation de Python 2.7

```apt-get install python2.7```

 2 - Installation de PIP

```apt-get install python-pip```

 3 - Installation des packages requis

>**WARNING** Si vous êtes sous Windows, supprimer mysql-python du fichier requirements.txt et installer le manuellement depuis [cette page](https://pypi.python.org/pypi/MySQL-python/1.2.5)

```
cd chemin/vers/TableauDeBord/
pip install -r requirements.txt
```

## Configuration de la base de données

Cet exemple ce base sur l'utilisation d'une table MySQL.

 1 - Créer une nouvelle table dans votre base de données.

 2 - Entrez vos paramètres de connexion dans `../plateforme_budgetaire/plateforme_budgetaire/settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #Pour utiliser une table MySQL
        'NAME': 'leNomDeLaBaseDeDonnée',
        'USER': 'votreNomDutilisateur',
        'PASSWORD': 'votreMotDePasse',
        'HOST': 'localhost',
    }
}
```
 3 - Mettez à jour votre base de données

 ```
 cd ../chemin/vers/plateforme_budgetaire/
 python manage.py migrate
 ```

# Lancement de votre application

 1 - Lancer votre serveur
 ```
 cd ../chemin/vers/TableauDeBord/
 python manage.py runserver
 ```

 2 - Rendez-vous à l'addresse `127.0.0.1:8000` avec votre navigateur