from datetime import datetime


class Intervention:
    """
    Modèle représentant une intervention
    d'un technicien sur un incident
    """
    def __init__(self, commentaire, duree_minutes,
                 incident_id, technicien_id,
                 id=None, date_intervention=None,
                 technicien_nom=None,
                 incident_titre=None):
        self.id = id
        self.commentaire = commentaire
        self.duree_minutes = duree_minutes
        self.incident_id = incident_id
        self.technicien_id = technicien_id
        self.date_intervention = date_intervention or datetime.now()
        self.technicien_nom = technicien_nom    # bonus affichage
        self.incident_titre = incident_titre    # bonus affichage

    def duree_en_heures(self):
        """Convertit la durée en heures"""
        return self.duree_minutes / 60

    def __str__(self):
        return (f"Intervention de {self.duree_minutes} min "
                f"- {self.commentaire[:50]}")

    def __repr__(self):
        return (f"Intervention(id={self.id}, "
                f"incident_id={self.incident_id}, "
                f"technicien_id={self.technicien_id})")