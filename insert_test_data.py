from dao.utilisateur_dao import UtilisateurDAO
from models.utilisateur import Utilisateur, Role


def inserer_donnees_test():
    """Insère des données de test"""
    dao = UtilisateurDAO()

    print("=== Insertion des données de test ===\n")

    # ─────────────────────────────────────
    # Créer un ADMIN
    # ─────────────────────────────────────
    admin = Utilisateur(
        login="admin",
        password="admin123",
        nom="Diallo",
        prenom="Mamadou",
        email="admin@isi.sn",
        role=Role.ADMIN.value,
        service="Informatique"
    )
    dao.ajouter(admin)

    # ─────────────────────────────────────
    # Créer des TECHNICIENS
    # ─────────────────────────────────────
    tech1 = Utilisateur(
        login="tech1",
        password="tech123",
        nom="Dieng",
        prenom="Aminata",
        email="aminata@isi.sn",
        role=Role.TECHNICIEN.value,
        service="Support"
    )
    dao.ajouter(tech1)

    tech2 = Utilisateur(
        login="tech2",
        password="tech123",
        nom="Fall",
        prenom="Moussa",
        email="moussa@isi.sn",
        role=Role.TECHNICIEN.value,
        service="Support"
    )
    dao.ajouter(tech2)

    # ─────────────────────────────────────
    # Créer des UTILISATEURS
    # ─────────────────────────────────────
    user1 = Utilisateur(
        login="user1",
        password="user123",
        nom="Sow",
        prenom="Fatou",
        email="fatou@isi.sn",
        role=Role.UTILISATEUR.value,
        service="Comptabilité"
    )
    dao.ajouter(user1)

    user2 = Utilisateur(
        login="user2",
        password="user123",
        nom="Ndiaye",
        prenom="Ibrahima",
        email="ibrahima@isi.sn",
        role=Role.UTILISATEUR.value,
        service="RH"
    )
    dao.ajouter(user2)

    print("\n✅ Données de test insérées avec succès !")
    print("\n=== Comptes disponibles ===")
    print("ADMIN      : login=admin   password=admin123")
    print("TECHNICIEN : login=tech1   password=tech123")
    print("TECHNICIEN : login=tech2   password=tech123")
    print("UTILISATEUR: login=user1   password=user123")
    print("UTILISATEUR: login=user2   password=user123")


if __name__ == "__main__":
    inserer_donnees_test()