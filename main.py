from menu.auth import Auth
from menu.interface import lancer_interface


def main():
    """Point d'entrée principal"""
    auth = Auth()

    # Authentification
    utilisateur = auth.connexion()

    if utilisateur:
        # Lancer le bon menu
        lancer_interface(utilisateur)
        # Déconnexion
        auth.deconnexion()
    else:
        print("❌ Authentification échouée")


if __name__ == "__main__":
    main()