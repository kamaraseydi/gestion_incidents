import psycopg2
from psycopg2 import OperationalError
from database.config import DB_CONFIG


class DatabaseConnection:
    """
    Singleton — une seule instance de connexion
    dans toute l'application
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialiser()
        return cls._instance

    def _initialiser(self):
        """Initialise les paramètres depuis config.py"""
        self._host = DB_CONFIG["host"]
        self._database = DB_CONFIG["database"]
        self._user = DB_CONFIG["user"]
        self._password = DB_CONFIG["password"]
        self._port = DB_CONFIG["port"]

    def get_connexion(self):
        """Retourne une nouvelle connexion à la BD"""
        try:
            connexion = psycopg2.connect(
                host=self._host,
                database=self._database,
                user=self._user,
                password=self._password,
                port=self._port
            )
            return connexion
        except OperationalError as e:
            print(f"❌ Erreur de connexion : {e}")
            return None

    def tester_connexion(self):
        """Teste si la connexion fonctionne"""
        conn = self.get_connexion()
        if conn:
            print("✅ Connexion réussie !")
            conn.close()
            return True
        print("❌ Connexion échouée")
        return False