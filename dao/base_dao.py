from abc import ABC, abstractmethod
from database.connexion import DatabaseConnection


class BaseDAO(ABC):
    """
    Classe abstraite de base pour tous les DAO
    Chaque DAO hérite de cette classe
    """

    def __init__(self):
        self.db = DatabaseConnection()  # Singleton

    @abstractmethod
    def ajouter(self, objet):
        """Ajouter un enregistrement"""
        pass

    @abstractmethod
    def trouver_par_id(self, id):
        """Trouver un enregistrement par ID"""
        pass

    @abstractmethod
    def modifier(self, objet):
        """Modifier un enregistrement"""
        pass

    @abstractmethod
    def supprimer(self, id):
        """Supprimer un enregistrement"""
        pass

    def get_tous(self, table):
        """
        Méthode générique → récupère tous les enregistrements
        Réutilisable par tous les DAO enfants
        """
        conn = self.db.get_connexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def supprimer_par_id(self, table, id):
        """
        Méthode générique → supprime par ID
        Réutilisable par tous les DAO enfants
        """
        conn = self.db.get_connexion()
        if conn is None:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {table} WHERE id = %s RETURNING id",
                (id,)
            )
            result = cursor.fetchone()
            conn.commit()

            if result:
                print(f"✅ Enregistrement ID {id} supprimé")
                return True
            else:
                print(f"❌ ID {id} non trouvé")
                return False

        except Exception as e:
            print(f"❌ Erreur : {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()