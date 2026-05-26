from enum import Enum
from datetime import date


class Role(Enum):
    UTILISATEUR = "UTILISATEUR"
    TECHNICIEN = "TECHNICIEN"
    ADMIN = "ADMIN"


class Utilisateur:
    """
    Modèle représentant un utilisateur du système
    Pas de SQL ici → juste les données
    """
    def __init__(self, login, password, nom, prenom,
                 email, role, service,
                 id=None, date_creation=None):
        self.id = id
        self.login = login
        self.password = password
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.role = role  # Role.ADMIN, Role.TECHNICIEN...
        self.service = service
        self.date_creation = date_creation or date.today()

    def est_admin(self):
        return self.role == Role.ADMIN.value

    def est_technicien(self):
        return self.role == Role.TECHNICIEN.value

    def est_utilisateur(self):
        return self.role == Role.UTILISATEUR.value

    def __str__(self):
        return (f"{self.prenom} {self.nom} "
                f"({self.role}) - {self.service}")

    def __repr__(self):
        return (f"Utilisateur(id={self.id}, "
                f"login={self.login}, "
                f"role={self.role})")