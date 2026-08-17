# gestion_incidents
Gestion des Tickets d'Incidents - L2 GL ISI


Application console de gestion des incidents 
informatiques développée en Python avec PostgreSQL.

## 📋 Description

La DSI d'une entreprise sénégalaise souhaite mettre 
en place un système de gestion des incidents (Help Desk).
Cette application permet :
- Aux **utilisateurs** de signaler des incidents
- Aux **techniciens** de prendre en charge et résoudre
- À l'**administrateur** de gérer et superviser

## 🏗️ Architecture

gestion_incidents/
├── database/
│ ├── config.py → Configuration BD
│ └── connexion.py → Singleton connexion
├── models/
│ ├── utilisateur.py → Modèle Utilisateur
│ ├── incident.py → Modèle Incident
│ └── intervention.py → Modèle Intervention
├── dao/
│ ├── base_dao.py → Classe abstraite DAO
│ ├── utilisateur_dao.py → CRUD Utilisateur
│ ├── incident_dao.py → CRUD Incident
│ └── intervention_dao.py→ CRUD Intervention
├── menu/
│ ├── auth.py → Authentification
│ └── interface.py → Menus par rôle
├── create_tables.py → Création des tables
├── insert_test_data.py → Données de test
└── main.py → Point d'entrée

## 🛠️ Technologies utilisées

- **Python 3.13**
- **PostgreSQL 16**
- **psycopg2-binary** 2.9.12

## ⚙️ Installation

### Prérequis
- Python 3.10+
- PostgreSQL 16
- pip

### Étapes

**1. Cloner le repository**
```bash
git clone https://github.com/kamaraseydi/gestion_incidents.git
cd gestion_incidents
```

**2. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**3. Configurer la base de données**

Copier le fichier de configuration :
```bash
cp database/config.exemple.py database/config.py
```

Modifier `database/config.py` avec vos paramètres :
```python
DB_CONFIG = {
    "host": "localhost",
    "database": "gestion_incidents",
    "user": "votre_user",
    "password": "votre_password",
    "port": "5432"
}
```

Créer la base de données dans PostgreSQL :
```sql
CREATE DATABASE gestion_incidents OWNER votre_user;
GRANT ALL PRIVILEGES ON DATABASE gestion_incidents TO votre_user;
```

**4. Créer les tables**
```bash
python create_tables.py
```

**5. Insérer les données de test**
```bash
python insert_test_data.py
```

**6. Lancer l'application**
```bash
python main.py
```

## 👤 Comptes de test

| Login  | Password  | Rôle        |
|--------|-----------|-------------|
| admin  | admin123  | ADMIN       |
| tech1  | tech123   | TECHNICIEN  |
| tech2  | tech123   | TECHNICIEN  |
| user1  | user123   | UTILISATEUR |
| user2  | user123   | UTILISATEUR |

## 🔄 Workflow des incidents

OUVERT → EN_COURS → RESOLU → FERME

- **OUVERT** → incident créé par un utilisateur
- **EN_COURS** → pris en charge par un technicien
- **RESOLU** → résolu par un technicien
- **FERME** → fermé définitivement

## 📊 Fonctionnalités par rôle

### UTILISATEUR
- Créer un incident
- Consulter ses incidents
- Filtrer par statut et priorité
- Voir le détail avec les interventions

### TECHNICIEN
- Voir tous les incidents ouverts/en cours
- Prendre en charge un incident
- Ajouter des interventions
- Résoudre et fermer des incidents

### ADMIN
- Toutes les fonctionnalités TECHNICIEN
- Gestion complète des utilisateurs (CRUD)
- Consulter tous les incidents
- Statistiques et rapports

## 🏛️ Concepts POO utilisés

- **Singleton** : classe DatabaseConnection
- **Héritage** : BaseDAO → UtilisateurDAO, IncidentDAO...
- **Classe abstraite** : BaseDAO avec @abstractmethod
- **Encapsulation** : attributs privés dans les modèles
- **Polymorphisme** : méthodes redéfinies dans chaque DAO

## 👨‍💻 Auteur

**Seydi Kamara** et **Mouhamed Diop**
- GitHub : [@kamaraseydi](https://github.com/kamaraseydi)
- Licence 2 - Génie Logiciel
- ISI Dakar - 2025
