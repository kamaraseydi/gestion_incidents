from dao.base_dao import BaseDAO
from models.intervention import Intervention


class InterventionDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    # ─────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────
    def ajouter(self, intervention: Intervention):
        """
        Ajoute une intervention
        Vérifie que l'incident est OUVERT ou EN_COURS
        """
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()

            # Vérifier le statut de l'incident
            cursor.execute("""
                SELECT statut FROM incident
                WHERE id = %s
            """, (intervention.incident_id,))

            row = cursor.fetchone()
            if not row:
                print("❌ Incident non trouvé")
                return None

            statut = row[0]
            if statut not in ('OUVERT', 'EN_COURS'):
                print(f"❌ Impossible d'intervenir : "
                      f"incident {statut}")
                return None

            # Ajouter l'intervention
            cursor.execute("""
                INSERT INTO intervention
                    (commentaire, duree_minutes,
                     incident_id, technicien_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, date_intervention
            """, (
                intervention.commentaire,
                intervention.duree_minutes,
                intervention.incident_id,
                intervention.technicien_id
            ))

            row = cursor.fetchone()
            intervention.id = row[0]
            intervention.date_intervention = row[1]
            conn.commit()
            print(f"✅ Intervention ajoutée ID: {intervention.id}")
            return intervention

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
    def trouver_par_id(self, id) -> Intervention:
        """Trouve une intervention par ID"""
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT iv.id, iv.commentaire,
                       iv.duree_minutes,
                       iv.date_intervention,
                       iv.incident_id,
                       iv.technicien_id,
                       u.nom, u.prenom,
                       i.titre
                FROM intervention iv
                JOIN utilisateur u ON iv.technicien_id = u.id
                JOIN incident i ON iv.incident_id = i.id
                WHERE iv.id = %s
            """, (id,))

            row = cursor.fetchone()
            if row:
                return Intervention(
                    id=row[0],
                    commentaire=row[1],
                    duree_minutes=row[2],
                    date_intervention=row[3],
                    incident_id=row[4],
                    technicien_id=row[5],
                    technicien_nom=f"{row[7]} {row[6]}",
                    incident_titre=row[8]
                )
            return None

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_par_incident(self, incident_id):
        """
        Retourne toutes les interventions
        d'un incident
        """
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT iv.id, iv.commentaire,
                       iv.duree_minutes,
                       iv.date_intervention,
                       iv.incident_id,
                       iv.technicien_id,
                       u.nom, u.prenom
                FROM intervention iv
                JOIN utilisateur u ON iv.technicien_id = u.id
                WHERE iv.incident_id = %s
                ORDER BY iv.date_intervention ASC
            """, (incident_id,))

            rows = cursor.fetchall()
            interventions = []
            for row in rows:
                interventions.append(Intervention(
                    id=row[0],
                    commentaire=row[1],
                    duree_minutes=row[2],
                    date_intervention=row[3],
                    incident_id=row[4],
                    technicien_id=row[5],
                    technicien_nom=f"{row[7]} {row[6]}"
                ))
            return interventions

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_par_technicien(self, technicien_id):
        """
        Retourne toutes les interventions
        d'un technicien
        """
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT iv.id, iv.commentaire,
                       iv.duree_minutes,
                       iv.date_intervention,
                       iv.incident_id,
                       iv.technicien_id,
                       i.titre, i.statut
                FROM intervention iv
                JOIN incident i ON iv.incident_id = i.id
                WHERE iv.technicien_id = %s
                ORDER BY iv.date_intervention DESC
            """, (technicien_id,))

            rows = cursor.fetchall()
            interventions = []
            for row in rows:
                intervention = Intervention(
                    id=row[0],
                    commentaire=row[1],
                    duree_minutes=row[2],
                    date_intervention=row[3],
                    incident_id=row[4],
                    technicien_id=row[5],
                    incident_titre=row[6]
                )
                intervention.incident_statut = row[7]
                interventions.append(intervention)
            return interventions

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_tous(self):
        """Retourne toutes les interventions"""
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT iv.id, iv.commentaire,
                       iv.duree_minutes,
                       iv.date_intervention,
                       iv.incident_id,
                       iv.technicien_id,
                       u.nom, u.prenom,
                       i.titre
                FROM intervention iv
                JOIN utilisateur u ON iv.technicien_id = u.id
                JOIN incident i ON iv.incident_id = i.id
                ORDER BY iv.date_intervention DESC
            """)

            rows = cursor.fetchall()
            interventions = []
            for row in rows:
                interventions.append(Intervention(
                    id=row[0],
                    commentaire=row[1],
                    duree_minutes=row[2],
                    date_intervention=row[3],
                    incident_id=row[4],
                    technicien_id=row[5],
                    technicien_nom=f"{row[7]} {row[6]}",
                    incident_titre=row[8]
                ))
            return interventions

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # STATISTIQUES
    # ─────────────────────────────────────
    def stats_par_technicien(self):
        """
        Pour l'admin :
        Nombre d'interventions et temps moyen
        par technicien
        """
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.nom, u.prenom,
                       COUNT(iv.id) as nb_interventions,
                       AVG(iv.duree_minutes) as duree_moyenne,
                       SUM(iv.duree_minutes) as duree_totale
                FROM utilisateur u
                LEFT JOIN intervention iv ON u.id = iv.technicien_id
                WHERE u.role = 'TECHNICIEN'
                GROUP BY u.id, u.nom, u.prenom
                ORDER BY nb_interventions DESC
            """)

            rows = cursor.fetchall()
            stats = []
            for row in rows:
                stats.append({
                    "id": row[0],
                    "nom": f"{row[2]} {row[1]}",
                    "nb_interventions": row[3],
                    "duree_moyenne": round(float(row[4]), 2)
                             if row[4] else 0,
                    "duree_totale": row[5] or 0
                })
            return stats

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────
    def modifier(self, intervention: Intervention):
        """Modifie une intervention"""
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE intervention
                SET commentaire = %s,
                    duree_minutes = %s
                WHERE id = %s
            """, (
                intervention.commentaire,
                intervention.duree_minutes,
                intervention.id
            ))

            conn.commit()
            print(f"✅ Intervention ID {intervention.id} modifiée")
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
        """Supprime une intervention"""
        return self.supprimer_par_id("intervention", id)