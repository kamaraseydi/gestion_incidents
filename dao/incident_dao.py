from dao.base_dao import BaseDAO
from models.incident import Incident, Statut


class IncidentDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    # ─────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────
    def ajouter(self, incident: Incident):
        """Crée un nouvel incident"""
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO incident
                    (titre, description, priorite,
                     statut, utilisateur_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, date_creation
            """, (
                incident.titre,
                incident.description,
                incident.priorite,
                incident.statut,
                incident.utilisateur_id
            ))

            row = cursor.fetchone()
            incident.id = row[0]
            incident.date_creation = row[1]
            conn.commit()
            print(f"✅ Incident '{incident.titre}' créé ID: {incident.id}")
            return incident

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # READ
    # ─────────────────────────────────────
    def trouver_par_id(self, id) -> Incident:
        """Trouve un incident par ID"""
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.titre, i.description,
                       i.priorite, i.statut,
                       i.date_creation, i.utilisateur_id,
                       u.nom, u.prenom
                FROM incident i
                JOIN utilisateur u ON i.utilisateur_id = u.id
                WHERE i.id = %s
            """, (id,))

            row = cursor.fetchone()
            if row:
                incident = Incident(
                    id=row[0],
                    titre=row[1],
                    description=row[2],
                    priorite=row[3],
                    statut=row[4],
                    date_creation=row[5],
                    utilisateur_id=row[6],
                    utilisateur_nom=f"{row[8]} {row[7]}"
                )
                return incident
            return None

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_tous(self):
        """Retourne tous les incidents"""
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.titre, i.description,
                       i.priorite, i.statut,
                       i.date_creation, i.utilisateur_id,
                       u.nom, u.prenom
                FROM incident i
                JOIN utilisateur u ON i.utilisateur_id = u.id
                ORDER BY i.date_creation DESC
            """)

            rows = cursor.fetchall()
            incidents = []
            for row in rows:
                incidents.append(Incident(
                    id=row[0],
                    titre=row[1],
                    description=row[2],
                    priorite=row[3],
                    statut=row[4],
                    date_creation=row[5],
                    utilisateur_id=row[6],
                    utilisateur_nom=f"{row[8]} {row[7]}"
                ))
            return incidents

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_par_utilisateur(self, utilisateur_id):
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.titre, i.description,
                       i.priorite, i.statut,
                       i.date_creation, i.utilisateur_id,
                       u.nom, u.prenom
                FROM incident i
                JOIN utilisateur u ON i.utilisateur_id = u.id
                WHERE i.utilisateur_id = %s
                ORDER BY i.date_creation DESC
            """, (utilisateur_id,))

            rows = cursor.fetchall()
            incidents = []
            for row in rows:
                incidents.append(Incident(
                    id=row[0],
                    titre=row[1],
                    description=row[2],
                    priorite=row[3],
                    statut=row[4],
                    date_creation=row[5],
                    utilisateur_id=row[6],
                    utilisateur_nom=f"{row[8]} {row[7]}"  # ✅ ajouté
                ))
            return incidents

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_par_statut(self, statut, utilisateur_id=None):
        """
        Retourne les incidents par statut
        Si utilisateur_id → filtre par utilisateur
        """
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()

            if utilisateur_id:
                cursor.execute("""
                    SELECT id, titre, description,
                           priorite, statut,
                           date_creation, utilisateur_id
                    FROM incident
                    WHERE statut = %s
                    AND utilisateur_id = %s
                    ORDER BY date_creation DESC
                """, (statut, utilisateur_id))
            else:
                cursor.execute("""
                    SELECT i.id, i.titre, i.description,
                           i.priorite, i.statut,
                           i.date_creation, i.utilisateur_id,
                           u.nom, u.prenom
                    FROM incident i
                    JOIN utilisateur u ON i.utilisateur_id = u.id
                    WHERE i.statut = %s
                    ORDER BY i.date_creation DESC
                """, (statut,))

            rows = cursor.fetchall()
            incidents = []
            for row in rows:
                if utilisateur_id:
                    incidents.append(Incident(
                        id=row[0],
                        titre=row[1],
                        description=row[2],
                        priorite=row[3],
                        statut=row[4],
                        date_creation=row[5],
                        utilisateur_id=row[6]
                    ))
                else:
                    incidents.append(Incident(
                        id=row[0],
                        titre=row[1],
                        description=row[2],
                        priorite=row[3],
                        statut=row[4],
                        date_creation=row[5],
                        utilisateur_id=row[6],
                        utilisateur_nom=f"{row[8]} {row[7]}"
                    ))
            return incidents

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_par_priorite(self, priorite, utilisateur_id=None):
        """Retourne les incidents par priorité"""
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()

            if utilisateur_id:
                cursor.execute("""
                    SELECT id, titre, description,
                           priorite, statut,
                           date_creation, utilisateur_id
                    FROM incident
                    WHERE priorite = %s
                    AND utilisateur_id = %s
                    ORDER BY date_creation DESC
                """, (priorite, utilisateur_id))
            else:
                cursor.execute("""
                    SELECT id, titre, description,
                           priorite, statut,
                           date_creation, utilisateur_id
                    FROM incident
                    WHERE priorite = %s
                    ORDER BY date_creation DESC
                """, (priorite,))

            rows = cursor.fetchall()
            incidents = []
            for row in rows:
                incidents.append(Incident(
                    id=row[0],
                    titre=row[1],
                    description=row[2],
                    priorite=row[3],
                    statut=row[4],
                    date_creation=row[5],
                    utilisateur_id=row[6]
                ))
            return incidents

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_ouverts_et_en_cours(self):
        """
        Retourne les incidents OUVERTS et EN_COURS
        Pour les techniciens
        """
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.titre, i.description,
                       i.priorite, i.statut,
                       i.date_creation, i.utilisateur_id,
                       u.nom, u.prenom
                FROM incident i
                JOIN utilisateur u ON i.utilisateur_id = u.id
                WHERE i.statut IN ('OUVERT', 'EN_COURS')
                ORDER BY
                    CASE i.priorite
                        WHEN 'CRITIQUE' THEN 1
                        WHEN 'HAUTE' THEN 2
                        WHEN 'MOYENNE' THEN 3
                        WHEN 'BASSE' THEN 4
                    END,
                    i.date_creation ASC
            """)

            rows = cursor.fetchall()
            incidents = []
            for row in rows:
                incidents.append(Incident(
                    id=row[0],
                    titre=row[1],
                    description=row[2],
                    priorite=row[3],
                    statut=row[4],
                    date_creation=row[5],
                    utilisateur_id=row[6],
                    utilisateur_nom=f"{row[8]} {row[7]}"
                ))
            return incidents

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────
    def modifier(self, incident: Incident):
        """Modifie un incident"""
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE incident
                SET titre = %s, description = %s,
                    priorite = %s
                WHERE id = %s
            """, (
                incident.titre,
                incident.description,
                incident.priorite,
                incident.id
            ))

            conn.commit()
            print(f"✅ Incident ID {incident.id} modifié")
            return True

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def changer_statut(self, incident_id, nouveau_statut):
        """
        Change le statut d'un incident
        Respecte le workflow :
        OUVERT → EN_COURS → RESOLU → FERME
        """
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()

            # Récupérer le statut actuel
            cursor.execute("""
                SELECT statut FROM incident
                WHERE id = %s
            """, (incident_id,))

            row = cursor.fetchone()
            if not row:
                print(f"❌ Incident non trouvé")
                return False

            statut_actuel = row[0]

            # Vérifier le workflow
            transitions_valides = {
                'OUVERT': 'EN_COURS',
                'EN_COURS': 'RESOLU',
                'RESOLU': 'FERME'
            }

            if transitions_valides.get(statut_actuel) != nouveau_statut:
                print(f"❌ Transition invalide : "
                      f"{statut_actuel} → {nouveau_statut}")
                return False

            # Changer le statut
            cursor.execute("""
                UPDATE incident
                SET statut = %s
                WHERE id = %s
            """, (nouveau_statut, incident_id))

            conn.commit()
            print(f"✅ Statut changé : "
                  f"{statut_actuel} → {nouveau_statut}")
            return True

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────
    def supprimer(self, id):
        """
        Supprime un incident
        Seulement s'il n'a pas d'interventions
        """
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()

            # Vérifier les interventions
            cursor.execute("""
                SELECT COUNT(*) FROM intervention
                WHERE incident_id = %s
            """, (id,))

            nb = cursor.fetchone()[0]
            if nb > 0:
                print(f"❌ Impossible : {nb} intervention(s) liée(s)")
                return False

            cursor.execute("""
                DELETE FROM incident
                WHERE id = %s
                RETURNING id
            """, (id,))

            result = cursor.fetchone()
            conn.commit()

            if result:
                print(f"✅ Incident ID {id} supprimé")
                return True
            else:
                print(f"❌ Incident non trouvé")
                return False

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def stats_par_statut(self):
        """Nombre d'incidents par statut"""
        conn = self.db.get_connexion()
        if conn is None:
            return {}
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT statut, COUNT(*) as total
                FROM incident
                GROUP BY statut
                ORDER BY statut
            """)
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows}

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    def stats_par_priorite(self):
        """Nombre d'incidents par priorité"""
        conn = self.db.get_connexion()
        if conn is None:
            return {}
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT priorite, COUNT(*) as total
                FROM incident
                GROUP BY priorite
                ORDER BY priorite
            """)
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows}

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    def taux_resolution_48h(self):
        """
        Taux d'incidents résolus en moins de 48h
        Pourcentage sur tous les incidents résolus
        """
        conn = self.db.get_connexion()
        if conn is None:
            return 0
        try:
            cursor = conn.cursor()

            # Total incidents résolus ou fermés
            cursor.execute("""
                SELECT COUNT(*) FROM incident
                WHERE statut IN ('RESOLU', 'FERME')
            """)
            total_resolus = cursor.fetchone()[0]

            if total_resolus == 0:
                return 0

            # Incidents résolus en moins de 48h
            cursor.execute("""
                SELECT COUNT(DISTINCT i.id)
                FROM incident i
                JOIN intervention iv ON i.id = iv.incident_id
                WHERE i.statut IN ('RESOLU', 'FERME')
                AND EXTRACT(EPOCH FROM (
                    iv.date_intervention - i.date_creation
                )) / 3600 <= 48
            """)
            resolus_48h = cursor.fetchone()[0]

            taux = (resolus_48h / total_resolus) * 100
            return round(taux, 2)

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return 0
        finally:
            cursor.close()
            conn.close()

    def temps_moyen_resolution(self):
        """
        Temps moyen de résolution en heures
        """
        conn = self.db.get_connexion()
        if conn is None:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT AVG(
                    EXTRACT(EPOCH FROM (
                        iv.date_intervention - i.date_creation
                    )) / 3600
                ) as temps_moyen
                FROM incident i
                JOIN intervention iv ON i.id = iv.incident_id
                WHERE i.statut IN ('RESOLU', 'FERME')
            """)
            row = cursor.fetchone()
            if row and row[0]:
                return round(float(row[0]), 2)
            return 0

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return 0
        finally:
            cursor.close()
            conn.close()