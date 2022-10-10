# Projet P8 : Créer une plateforme pour amateur de Nutella 

Code source : https://github.com/nicoseng/P8_purbeurre
Programme rédigé sous Python3. Projet sous Virtual Env et Git 
Adresse de l’application web sur heroku : https://purbeurre-website.herokuapp.com/

# I°) Télécharger le projet sur votre répertoire local

```
git clone https://github.com/nicoseng/P8_purbeurre.git
```

# II°) Préparez l’environnement virtuel de développement

1.  Installez un environnement virtuel de développement depuis votre terminal. (python3 –m venv venv) ;
2.  Activez l’environnement virtuel en tapant selon votre situation :
		- pour Unix/MacOS :  `source venv/bin/activate`
		- pour Windows : `venv\Scripts\activate.bat`

Une mention (venv) s’affiche à gauche de votre console indiquant la bonne activation de votre environnement virtuel.

# III°) Installer les dépendances du projet

```
pip install -r requirements.txt
```
# IV°) Ajouter les données dans l'application

Dans le terminal, entrez la commande heroku run python manage.py insert_category. 
Cette commande permet d'ajouter les données catégories nécessaires afin pouvoir effectuer des recherches de produits.
Dans le terminal, entrez la commande heroku run python manage.py insert_products. 
Cette commande permet d'ajouter les données produits nécessaires afin pouvoir effectuer des recherches de produits.


# V°) Démarrer l'application

Dans le terminal, entrez la commande heroku open. Cette commande permet de se connecter à l'adresse URL où est hébergé l'application sur heroku : https://purbeurre-website.herokuapp.com/

# VI°) Gérer l'application depuis django admin

Dans votre terminal, créer un super utilisateur (superuser) permet de pouvoir gérer votre application via une fenêtre d'administration Django. Pour ce faire, taper la commande suivante :
```
heroku run python manage.py cretesuperuser
```
puis suivre les instructions fournies par la suite (username, password, etc.) 

Rendez-vous dans https://purbeurre-website.herokuapp.com/admin afin de pouvoir vous connecter avec votre username et votre password nouvellement créées.