### AFTI CTF PROJECT ###

### Python : 
pip install django
pip install MySQL-python
pip install django-crispy-forms
pip install django-jquery

### General :

Dès votre connection, accédez à byobu en tapant : byobu.
Pour démarrer le serveur Django : python manage.py runserver
Pour resynchroniser la BDD DJango : python manage.py syncdb
Pour dumper la BDD MySQL : mysqldump -uk6 -pk6 k6 > dump_k6.sql
Pour réinjecter la BDD MySQL : mysql -uk6 -pK6 k6 < dump_k6.sql

### TODO-List :

- Revoir les forms -> Ranger tout bien dans forms.py...
- Revoir l'accueil (Bienvenue, remplir la page...) -> Kinda done, faudra faire des zolies zimages.
- Revoir la fonction de validation des épreuves (ne fonctionne pas en l'état actuel)
- Ajouter une fonction de tri par différents paramètres (pour les épreuves d'un point de vue admin, surtout) > ky0p working on it. 
- Trouver un nom de domaine (+ sous-domaines pour les conteneurs) -> hack6.fr est dispo. On peut imagine avoir web.hack6.fr, reverse.hack6.fr etc.
- Intégrer le logo + ajouter des couleurs, de la vie ! -> Kinda done, si vous voulez ajouter des trucs...
- Ajouter un champ "Avatar" pour les utilisateurs (+ description, adresse mail, site, etc...) > Un peu chiant à faire en l'état actuel, à voir. 
- Créer des épreuves... -> Everyone working on it. 
