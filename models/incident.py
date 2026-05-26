from enum import Enum
from datetime import datetime


class Priorite(Enum):
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"


class Statut(Enum):
    OUVERT = "OUVERT"
    EN_COURS = "EN_COURS"
    RESOLU = "RESOLU"
    FERME = "FERME"


class Incident:
    """
    Modèle représentant un incident informatique
    """
    def __init__(self, titre, description, priorite,
                 utilisateur_id,
                 id=None, statut=None,
                 date_creation=None,
                 utilisateur_nom=None):
        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut or Statut.OUVERT.value
        self.utilisateur_id = utilisateur_id
        self.date_creation = date_creation or datetime.now()
        self.utilisateur_nom = utilisateur_nom  # bonus affichage

    def peut_etre_pris_en_charge(self):
        """Vérifie si l'incident peut être pris en charge"""
        return self.statut == Statut.OUVERT.value

    def peut_etre_resolu(self):
        """Vérifie si l'incident peut être résolu"""
        return self.statut == Statut.EN_COURS.value

    def peut_etre_ferme(self):
        """Vérifie si l'incident peut être fermé"""
        return self.statut == Statut.RESOLU.value

    def __str__(self):
        return (f"Priorité [{self.priorite}] {self.titre} "
                f"- Statut: {self.statut}")

    def __repr__(self):
        return (f"Incident(id={self.id}, "
                f"titre={self.titre}, "
                f"statut={self.statut})")