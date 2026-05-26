from database.connexion import DatabaseConnection


def creer_tables():
    """Crée toutes les tables de la base de données"""
    db = DatabaseConnection()
    conn = db.get_connexion()

    if conn is None:
        print("❌ Impossible de se connecter à la BD")
        return

    try:
        cursor = conn.cursor()

        # ─────────────────────────────────────
        # Table utilisateur
        # ─────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilisateur (
                id SERIAL PRIMARY KEY,
                login VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL
                    CHECK (role IN ('UTILISATEUR', 'TECHNICIEN', 'ADMIN')),
                service VARCHAR(100),
                date_creation DATE DEFAULT CURRENT_DATE
            );
        """)
        print("✅ Table 'utilisateur' créée")

        # ─────────────────────────────────────
        # Table incident
        # ─────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incident (
                id SERIAL PRIMARY KEY,
                titre VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                priorite VARCHAR(20) NOT NULL
                    CHECK (priorite IN ('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE')),
                statut VARCHAR(20) NOT NULL DEFAULT 'OUVERT'
                    CHECK (statut IN ('OUVERT', 'EN_COURS', 'RESOLU', 'FERME')),
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                utilisateur_id INTEGER NOT NULL
                    REFERENCES utilisateur(id)
            );
        """)
        print("✅ Table 'incident' créée")

        # ─────────────────────────────────────
        # Table intervention
        # ─────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intervention (
                id SERIAL PRIMARY KEY,
                commentaire TEXT NOT NULL,
                duree_minutes INTEGER NOT NULL
                    CHECK (duree_minutes >= 0),
                date_intervention TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                incident_id INTEGER NOT NULL
                    REFERENCES incident(id),
                technicien_id INTEGER NOT NULL
                    REFERENCES utilisateur(id)
            );
        """)
        print("✅ Table 'intervention' créée")

        # Valider toutes les créations
        conn.commit()
        print("\n✅ Toutes les tables créées avec succès !")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()