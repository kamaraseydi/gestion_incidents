from dao.utilisateur_dao import UtilisateurDAO
from dao.incident_dao import IncidentDAO
from dao.intervention_dao import InterventionDAO
from models.utilisateur import Utilisateur, Role
from models.incident import Incident, Priorite, Statut
from models.intervention import Intervention


# ─────────────────────────────────────
# Instances DAO
# ─────────────────────────────────────
utilisateur_dao = UtilisateurDAO()
incident_dao = IncidentDAO()
intervention_dao = InterventionDAO()


def afficher_separateur():
    print("─" * 50)

def afficher_titre(titre):
    print("\n" + "═" * 50)
    print(f"   {titre}")
    print("═" * 50)

def saisir_entier(message):
    """Saisie sécurisée d'un entier"""
    try:
        return int(input(message))
    except ValueError:
        print("❌ Veuillez saisir un nombre entier")
        return None


def afficher_incidents(incidents):
    """Affiche une liste d'incidents"""
    if not incidents:
        print("Aucun incident trouvé")
        return

    afficher_separateur()
    print(f"{'ID':<5} {'Titre':<25} {'Priorité':<10} "
          f"{'Statut':<10} {'Signalé par':<15}")
    afficher_separateur()

    for i in incidents:
        # ✅ vérification None
        utilisateur_nom = getattr(i, 'utilisateur_nom', None)
        utilisateur_nom = utilisateur_nom if utilisateur_nom else 'N/A'

        print(f"{i.id:<5} {i.titre[:24]:<25} "
              f"{i.priorite:<10} {i.statut:<10} "
              f"{utilisateur_nom:<15}")
    afficher_separateur()


def menu_utilisateur(utilisateur):
    """Menu pour le rôle UTILISATEUR"""
    while True:
        afficher_titre(f"MENU UTILISATEUR — {utilisateur.prenom}")
        print("1. Créer un incident")
        print("2. Mes incidents")
        print("3. Filtrer par statut")
        print("4. Filtrer par priorité")
        print("5. Détail d'un incident")
        print("0. Se déconnecter")

        choix = saisir_entier("\nVotre choix : ")
        if choix is None:
            continue

        match choix:
            case 1:
                creer_incident(utilisateur)
            case 2:
                incidents = incident_dao.get_par_utilisateur(
                    utilisateur.id
                )
                afficher_incidents(incidents)
            case 3:
                filtrer_incidents_statut(utilisateur)
            case 4:
                filtrer_incidents_priorite(utilisateur)
            case 5:
                detail_incident(utilisateur)
            case 0:
                break
            case _:
                print("❌ Choix invalide")


def creer_incident(utilisateur):
    """Créer un nouvel incident"""
    afficher_titre("CRÉER UN INCIDENT")

    titre = input("Titre : ").strip()
    if not titre:
        print("❌ Titre obligatoire")
        return

    description = input("Description : ").strip()
    if not description:
        print("❌ Description obligatoire")
        return

    print("\nPriorités disponibles :")
    for p in Priorite:
        print(f"  → {p.value}")

    priorite = input("Priorité : ").strip().upper()
    if priorite not in [p.value for p in Priorite]:
        print("❌ Priorité invalide")
        return

    incident = Incident(
        titre=titre,
        description=description,
        priorite=priorite,
        utilisateur_id=utilisateur.id
    )
    incident_dao.ajouter(incident)


def filtrer_incidents_statut(utilisateur):
    """Filtre les incidents par statut"""
    afficher_titre("FILTRER PAR STATUT")

    print("Statuts disponibles :")
    for s in Statut:
        print(f"  → {s.value}")

    statut = input("Statut : ").strip().upper()
    if statut not in [s.value for s in Statut]:
        print("❌ Statut invalide")
        return

    incidents = incident_dao.get_par_statut(
        statut,
        utilisateur.id
    )
    afficher_incidents(incidents)


def filtrer_incidents_priorite(utilisateur):
    """Filtre les incidents par priorité"""
    afficher_titre("FILTRER PAR PRIORITÉ")

    print("Priorités disponibles :")
    for p in Priorite:
        print(f"  → {p.value}")

    priorite = input("Priorité : ").strip().upper()
    if priorite not in [p.value for p in Priorite]:
        print("❌ Priorité invalide")
        return

    incidents = incident_dao.get_par_priorite(
        priorite,
        utilisateur.id
    )
    afficher_incidents(incidents)


def detail_incident(utilisateur):
    """Affiche le détail d'un incident"""
    afficher_titre("DÉTAIL INCIDENT")

    id_incident = saisir_entier("ID de l'incident : ")
    if id_incident is None:
        return

    incident = incident_dao.trouver_par_id(id_incident)
    if not incident:
        print("❌ Incident non trouvé")
        return

    # Vérifier que c'est son incident
    if incident.utilisateur_id != utilisateur.id:
        print("❌ Accès refusé")
        return

    print(f"\n{'─'*50}")
    print(f"Titre       : {incident.titre}")
    print(f"Description : {incident.description}")
    print(f"Priorité    : {incident.priorite}")
    print(f"Statut      : {incident.statut}")
    print(f"Créé le     : {incident.date_creation}")

    # Afficher les interventions
    interventions = intervention_dao.get_par_incident(id_incident)
    if interventions:
        print(f"\n{'─'*50}")
        print("Interventions :")
        for iv in interventions:
            print(f"  → {iv.technicien_nom} "
                  f"({iv.duree_minutes} min) : "
                  f"{iv.commentaire}")


def menu_technicien(utilisateur):
    """Menu pour le rôle TECHNICIEN"""
    while True:
        afficher_titre(f"MENU TECHNICIEN — {utilisateur.prenom}")
        print("1. Incidents ouverts et en cours")
        print("2. Prendre en charge un incident")
        print("3. Ajouter une intervention")
        print("4. Résoudre un incident")
        print("5. Fermer un incident")
        print("6. Mes interventions")
        print("0. Se déconnecter")

        choix = saisir_entier("\nVotre choix : ")
        if choix is None:
            continue

        match choix:
            case 1:
                incidents = incident_dao.get_ouverts_et_en_cours()
                afficher_incidents(incidents)
            case 2:
                prendre_en_charge()
            case 3:
                ajouter_intervention(utilisateur)
            case 4:
                changer_statut_incident(Statut.RESOLU.value)
            case 5:
                changer_statut_incident(Statut.FERME.value)
            case 6:
                interventions = intervention_dao.get_par_technicien(
                    utilisateur.id
                )
                afficher_interventions(interventions)
            case 0:
                break
            case _:
                print("❌ Choix invalide")


def prendre_en_charge():
    """Prise en charge d'un incident"""
    afficher_titre("PRENDRE EN CHARGE")

    id_incident = saisir_entier("ID de l'incident : ")
    if id_incident is None:
        return

    incident_dao.changer_statut(
        id_incident,
        Statut.EN_COURS.value
    )


def ajouter_intervention(utilisateur):
    """Ajouter une intervention sur un incident"""
    afficher_titre("AJOUTER UNE INTERVENTION")

    id_incident = saisir_entier("ID de l'incident : ")
    if id_incident is None:
        return

    commentaire = input("Commentaire : ").strip()
    if not commentaire:
        print("❌ Commentaire obligatoire")
        return

    duree = saisir_entier("Durée (minutes) : ")
    if duree is None or duree < 0:
        print("❌ Durée invalide")
        return

    intervention = Intervention(
        commentaire=commentaire,
        duree_minutes=duree,
        incident_id=id_incident,
        technicien_id=utilisateur.id
    )
    intervention_dao.ajouter(intervention)


def changer_statut_incident(nouveau_statut):
    """Change le statut d'un incident"""
    afficher_titre(f"PASSER À {nouveau_statut}")

    id_incident = saisir_entier("ID de l'incident : ")
    if id_incident is None:
        return

    incident_dao.changer_statut(id_incident, nouveau_statut)


def afficher_interventions(interventions):
    """Affiche une liste d'interventions"""
    if not interventions:
        print("Aucune intervention trouvée")
        return

    afficher_separateur()
    print(f"{'ID':<5} {'Incident':<25} {'Durée':<10} "
          f"{'Date':<20}")
    afficher_separateur()

    for iv in interventions:
        titre = getattr(iv, 'incident_titre', 'N/A')
        print(f"{iv.id:<5} {titre[:24]:<25} "
              f"{iv.duree_minutes} min   "
              f"{str(iv.date_intervention)[:19]:<20}")
    afficher_separateur()



def menu_admin(utilisateur):
    """Menu pour le rôle ADMIN"""
    while True:
        afficher_titre(f"MENU ADMIN — {utilisateur.prenom}")
        print("1. Gestion des utilisateurs")
        print("2. Tous les incidents")
        print("3. Incidents ouverts et en cours")
        print("4. Prendre en charge un incident")
        print("5. Ajouter une intervention")
        print("6. Résoudre un incident")
        print("7. Fermer un incident")
        print("8. Statistiques et rapports")
        print("0. Se déconnecter")

        choix = saisir_entier("\nVotre choix : ")
        if choix is None:
            continue

        match choix:
            case 1:
                menu_gestion_utilisateurs()
            case 2:
                incidents = incident_dao.get_tous()
                afficher_incidents(incidents)
            case 3:
                incidents = incident_dao.get_ouverts_et_en_cours()
                afficher_incidents(incidents)
            case 4:
                prendre_en_charge()
            case 5:
                ajouter_intervention(utilisateur)
            case 6:
                changer_statut_incident(Statut.RESOLU.value)
            case 7:
                changer_statut_incident(Statut.FERME.value)
            case 8:
                menu_statistiques()
            case 0:
                break
            case _:
                print("❌ Choix invalide")


def menu_gestion_utilisateurs():
    """Gestion complète des utilisateurs"""
    while True:
        afficher_titre("GESTION DES UTILISATEURS")
        print("1. Lister tous les utilisateurs")
        print("2. Ajouter un utilisateur")
        print("3. Rechercher un utilisateur")
        print("4. Modifier un utilisateur")
        print("5. Supprimer un utilisateur")
        print("0. Retour")

        choix = saisir_entier("\nVotre choix : ")
        if choix is None:
            continue

        match choix:
            case 1:
                utilisateurs = utilisateur_dao.get_tous()
                afficher_utilisateurs(utilisateurs)
            case 2:
                ajouter_utilisateur()
            case 3:
                terme = input("Rechercher : ").strip()
                resultats = utilisateur_dao.rechercher(terme)
                afficher_utilisateurs(resultats)
            case 4:
                modifier_utilisateur()
            case 5:
                id_u = saisir_entier("ID à supprimer : ")
                if id_u:
                    utilisateur_dao.supprimer(id_u)
            case 0:
                break
            case _:
                print("❌ Choix invalide")


def afficher_utilisateurs(utilisateurs):
    """Affiche une liste d'utilisateurs"""
    if not utilisateurs:
        print("Aucun utilisateur trouvé")
        return

    afficher_separateur()
    print(f"{'ID':<5} {'Login':<15} {'Nom':<20} "
          f"{'Rôle':<15} {'Service':<15}")
    afficher_separateur()

    for u in utilisateurs:
        print(f"{u.id:<5} {u.login:<15} "
              f"{u.prenom} {u.nom:<15} "
              f"{u.role:<15} {u.service:<15}")
    afficher_separateur()


def ajouter_utilisateur():
    """Ajouter un nouvel utilisateur"""
    afficher_titre("AJOUTER UN UTILISATEUR")

    login = input("Login : ").strip()
    password = input("Mot de passe : ").strip()
    nom = input("Nom : ").strip().upper()
    prenom = input("Prénom : ").strip().capitalize()
    email = input("Email : ").strip()
    service = input("Service : ").strip()

    print("\nRôles disponibles :")
    for r in Role:
        print(f"  → {r.value}")
    role = input("Rôle : ").strip().upper()

    if role not in [r.value for r in Role]:
        print("❌ Rôle invalide")
        return

    u = Utilisateur(
        login=login,
        password=password,
        nom=nom,
        prenom=prenom,
        email=email,
        role=role,
        service=service
    )
    utilisateur_dao.ajouter(u)


def modifier_utilisateur():
    """Modifier un utilisateur"""
    afficher_titre("MODIFIER UN UTILISATEUR")

    id_u = saisir_entier("ID de l'utilisateur : ")
    if id_u is None:
        return

    u = utilisateur_dao.trouver_par_id(id_u)
    if not u:
        print("❌ Utilisateur non trouvé")
        return

    print(f"\nNom actuel : {u.nom}")
    nouveau_nom = input("Nouveau nom (Enter pour garder) : ").strip()
    if nouveau_nom:
        u.nom = nouveau_nom.upper()

    print(f"Prénom actuel : {u.prenom}")
    nouveau_prenom = input("Nouveau prénom (Enter pour garder) : ").strip()
    if nouveau_prenom:
        u.prenom = nouveau_prenom.capitalize()

    print(f"Email actuel : {u.email}")
    nouvel_email = input("Nouvel email (Enter pour garder) : ").strip()
    if nouvel_email:
        u.email = nouvel_email

    print(f"Service actuel : {u.service}")
    nouveau_service = input("Nouveau service (Enter pour garder) : ").strip()
    if nouveau_service:
        u.service = nouveau_service

    utilisateur_dao.modifier(u)


def menu_statistiques():
    """Statistiques pour l'admin"""
    afficher_titre("STATISTIQUES ET RAPPORTS")

    # Incidents par statut
    print("\n📊 Incidents par statut :")
    afficher_separateur()
    for statut in Statut:
        incidents = incident_dao.get_par_statut(statut.value)
        print(f"  {statut.value:<15} : {len(incidents)}")

    # Incidents par priorité
    print("\n📊 Incidents par priorité :")
    afficher_separateur()
    for priorite in Priorite:
        incidents = incident_dao.get_par_priorite(priorite.value)
        print(f"  {priorite.value:<15} : {len(incidents)}")

    # Top techniciens
    print("\n📊 Top techniciens :")
    afficher_separateur()
    print(f"{'Nom':<20} {'Interventions':<15} {'Durée moy (min)':<15}")
    afficher_separateur()
    stats = intervention_dao.stats_par_technicien()
    for i, s in enumerate(stats[:3], 1):
        print(f"{i}. {s['nom']:<20} "
              f"{s['nb_interventions']:<15} "
              f"{s['duree_moyenne']:<15}")

    input("\nAppuyez sur Entrée pour continuer...")


def lancer_interface(utilisateur):
    """
    Lance le bon menu selon le rôle
    de l'utilisateur connecté
    """
    if utilisateur.role == Role.ADMIN.value:
        menu_admin(utilisateur)
    elif utilisateur.role == Role.TECHNICIEN.value:
        menu_technicien(utilisateur)
    elif utilisateur.role == Role.UTILISATEUR.value:
        menu_utilisateur(utilisateur)
    else:
        print(f"❌ Rôle inconnu : {utilisateur.role}")


