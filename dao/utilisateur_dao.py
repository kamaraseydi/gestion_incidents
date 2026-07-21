from dao.base_dao import BaseDAO
from models.utilisateur import Utilisateur


class UtilisateurDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    # ─────────────────────────────────────
    # AUTHENTIFICATION
    # ─────────────────────────────────────
    def authentifier(self, login, password) -> Utilisateur:
        """
        Vérifie login et password
        Retourne l'utilisateur si correct
        Sinon retourne None
        """
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, login, password, nom, prenom,
                       email, role, service, date_creation
                FROM utilisateur
                WHERE login = %s AND password = %s
            """, (login, password))

            row = cursor.fetchone()
            if row:
                return Utilisateur(
                    id=row[0],
                    login=row[1],
                    password=row[2],
                    nom=row[3],
                    prenom=row[4],
                    email=row[5],
                    role=row[6],
                    service=row[7],
                    date_creation=row[8]
                )
            return None

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────
    def ajouter(self, utilisateur: Utilisateur):
        """Ajoute un utilisateur"""
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()

            # Vérifier si login existe déjà
            cursor.execute("""
                SELECT id FROM utilisateur
                WHERE login = %s
            """, (utilisateur.login,))

            if cursor.fetchone():
                print(f"❌ Login '{utilisateur.login}' déjà utilisé")
                return None

            cursor.execute("""
                INSERT INTO utilisateur
                    (login, password, nom, prenom,
                     email, role, service)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                utilisateur.login,
                utilisateur.password,
                utilisateur.nom,
                utilisateur.prenom,
                utilisateur.email,
                utilisateur.role,
                utilisateur.service
            ))

            utilisateur.id = cursor.fetchone()[0]
            conn.commit()
            print(f"✅ Utilisateur '{utilisateur.login}' créé")
            return utilisateur

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
    def trouver_par_id(self, id) -> Utilisateur:
        """Trouve un utilisateur par ID"""
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, login, password, nom, prenom,
                       email, role, service, date_creation
                FROM utilisateur
                WHERE id = %s
            """, (id,))

            row = cursor.fetchone()
            if row:
                return Utilisateur(
                    id=row[0],
                    login=row[1],
                    password=row[2],
                    nom=row[3],
                    prenom=row[4],
                    email=row[5],
                    role=row[6],
                    service=row[7],
                    date_creation=row[8]
                )
            return None

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def trouver_par_login(self, login) -> Utilisateur:
        """Trouve un utilisateur par login"""
        conn = self.db.get_connexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, login, password, nom, prenom,
                       email, role, service, date_creation
                FROM utilisateur
                WHERE login = %s
            """, (login,))

            row = cursor.fetchone()
            if row:
                return Utilisateur(
                    id=row[0],
                    login=row[1],
                    password=row[2],
                    nom=row[3],
                    prenom=row[4],
                    email=row[5],
                    role=row[6],
                    service=row[7],
                    date_creation=row[8]
                )
            return None

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_tous(self):
        """Retourne tous les utilisateurs"""
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, login, nom, prenom,
                       email, role, service
                FROM utilisateur
                ORDER BY nom, prenom
            """)

            rows = cursor.fetchall()
            utilisateurs = []
            for row in rows:
                utilisateurs.append(Utilisateur(
                    id=row[0],
                    login=row[1],
                    password="",
                    nom=row[2],
                    prenom=row[3],
                    email=row[4],
                    role=row[5],
                    service=row[6]
                ))
            return utilisateurs

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def rechercher(self, terme):
        """Recherche par nom, login ou service"""
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, login, nom, prenom,
                       email, role, service
                FROM utilisateur
                WHERE nom ILIKE %s
                   OR login ILIKE %s
                   OR service ILIKE %s
                ORDER BY nom
            """, (f'%{terme}%', f'%{terme}%', f'%{terme}%'))

            rows = cursor.fetchall()
            utilisateurs = []
            for row in rows:
                utilisateurs.append(Utilisateur(
                    id=row[0],
                    login=row[1],
                    password="",
                    nom=row[2],
                    prenom=row[3],
                    email=row[4],
                    role=row[5],
                    service=row[6]
                ))
            return utilisateurs

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_par_role(self, role):
        """Retourne tous les utilisateurs d'un rôle"""
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, login, nom, prenom,
                       email, role, service
                FROM utilisateur
                WHERE role = %s
                ORDER BY nom
            """, (role,))

            rows = cursor.fetchall()
            utilisateurs = []
            for row in rows:
                utilisateurs.append(Utilisateur(
                    id=row[0],
                    login=row[1],
                    password="",
                    nom=row[2],
                    prenom=row[3],
                    email=row[4],
                    role=row[5],
                    service=row[6]
                ))
            return utilisateurs

        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # ─────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────
    def modifier(self, utilisateur: Utilisateur):
        """Modifie un utilisateur"""
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE utilisateur
                SET nom = %s, prenom = %s,
                    email = %s, role = %s,
                    service = %s
                WHERE id = %s
            """, (
                utilisateur.nom,
                utilisateur.prenom,
                utilisateur.email,
                utilisateur.role,
                utilisateur.service,
                utilisateur.id
            ))

            conn.commit()
            print(f"✅ Utilisateur ID {utilisateur.id} modifié")
            return True

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def modifier_password(self, id, nouveau_password):
        """Modifie le mot de passe"""
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE utilisateur
                SET password = %s
                WHERE id = %s
            """, (nouveau_password, id))

            conn.commit()
            print(f"✅ Mot de passe modifié")
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
        Supprime un utilisateur
        Seulement s'il n'a pas d'incidents
        ou d'interventions
        """
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()

            # Vérifier les incidents
            cursor.execute("""
                SELECT COUNT(*) FROM incident
                WHERE utilisateur_id = %s
            """, (id,))
            nb_incidents = cursor.fetchone()[0]

            if nb_incidents > 0:
                print(f"❌ Impossible : {nb_incidents} "
                      f"incident(s) lié(s)")
                return False

            # Vérifier les interventions
            cursor.execute("""
                SELECT COUNT(*) FROM intervention
                WHERE technicien_id = %s
            """, (id,))
            nb_interventions = cursor.fetchone()[0]

            if nb_interventions > 0:
                print(f"❌ Impossible : {nb_interventions} "
                      f"intervention(s) liée(s)")
                return False

            # Suppression physique
            cursor.execute("""
                DELETE FROM utilisateur
                WHERE id = %s
                RETURNING id
            """, (id,))

            result = cursor.fetchone()
            conn.commit()

            if result:
                print(f"✅ Utilisateur ID {id} supprimé")
                return True
            else:
                print(f"❌ Utilisateur non trouvé")
                return False

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()