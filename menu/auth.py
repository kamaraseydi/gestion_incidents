from dao.utilisateur_dao import UtilisateurDAO


class Auth:
    """
    Gère l'authentification des utilisateurs
    """

    def __init__(self):
        self.dao = UtilisateurDAO()
        self.utilisateur_connecte = None

    def connexion(self):
        """
        Demande login/password
        Retourne l'utilisateur si correct
        """
        print("\n" + "═" * 40)
        print("   GESTION DES TICKETS D'INCIDENTS")
        print("═" * 40)
        print("   Veuillez vous connecter")
        print("═" * 40)

        # 3 tentatives maximum
        for tentative in range(3):
            print(f"\nTentative {tentative + 1}/3")
            login = input("Login : ").strip()
            password = input("Mot de passe : ").strip()

            if not login or not password:
                print("❌ Login et mot de passe obligatoires")
                continue

            utilisateur = self.dao.authentifier(login, password)

            if utilisateur:
                self.utilisateur_connecte = utilisateur
                print(f"\n✅ Bienvenue {utilisateur.prenom} "
                      f"{utilisateur.nom} !")
                print(f"   Rôle : {utilisateur.role}")
                return utilisateur
            else:
                print("❌ Login ou mot de passe incorrect")
                restantes = 2 - tentative
                if restantes > 0:
                    print(f"   {restantes} tentative(s) restante(s)")

        print("\n❌ Trop de tentatives échouées")
        print("   Application fermée")
        return None

    def deconnexion(self):
        """Déconnecte l'utilisateur"""
        if self.utilisateur_connecte:
            print(f"\n👋 Au revoir "
                  f"{self.utilisateur_connecte.prenom} "
                  f"{self.utilisateur_connecte.nom} !")
        self.utilisateur_connecte = None

    def est_connecte(self):
        """Vérifie si un utilisateur est connecté"""
        return self.utilisateur_connecte is not None

    def get_utilisateur(self):
        """Retourne l'utilisateur connecté"""
        return self.utilisateur_connecte