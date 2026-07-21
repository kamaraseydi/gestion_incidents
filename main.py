from create_tables import creer_tables
from insert_test_data import inserer_donnees_test
from menu.auth import Auth

# 1. Créer les tables
creer_tables()

# 2. Insérer les données de test
inserer_donnees_test()

# 3. Tester l'authentification
auth = Auth()
utilisateur = auth.connexion()

if utilisateur:
    print(f"\nConnecté en tant que : {utilisateur.role}")