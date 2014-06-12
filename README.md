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
# Pour le site :
- Revoir les forms -> Ranger tout bien dans forms.py...
- Revoir l'accueil (Bienvenue, remplir la page...) -> Kinda done, faudra faire des zolies zimages.
- Revoir la fonction de validation des épreuves (ne fonctionne pas en l'état actuel)
- Intégrer le logo + ajouter des couleurs, de la vie ! -> Kinda done, si vous voulez ajouter des trucs...
- Ajouter un champ "Avatar" pour les utilisateurs (+ description, adresse mail, site, etc...) > Un peu chiant à faire en l'état actuel, à voir. 
- Créer des épreuves... -> Everyone working on it. 
# Pour le serveur :
- Ajouter envoi de mail => ssmtp.
- Ajouter un google Analytics/Piwik ?
- Fixer les épreuves, containers LXC.
- Changer les passwords partout.
