import explore_dnb as dnb

#  Fonctions du Menu 

def afficher_menu():
    """Affiche le menu principal à l'utilisateur."""
    print("\n--- Consultation des résultats DNB ---")
    print("1: Meilleur et pire taux de réussite (tous collèges, toutes sessions)")
    print("2: Nombre d'admis pour une session donnée")
    print("3: Nombre de présents pour un département et une session")
    print("4: Taux de réussite d'un collège (session 2020)")
    print("5: Meilleur collège pour un département et une session")
    print("6: Plus longue période d'amélioration (national)")
    print("0: Quitter")

def charger_donnees(nom_fichier):
    """
    Charge les données en appelant la fonction de dnb_functions.
    (En supposant que dnb.charger_resultats fait la conversion des types)
    """
    try:
        resultats = dnb.charger_resultats(nom_fichier)
    except FileNotFoundError:
        print(f"ERREUR: Le fichier '{nom_fichier}' est introuvable.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier: {e}")
        return None

    return resultats

def programme_principal():
    NOM_FICHIER = "dnb1.csv"
    """Fonction principale du programme de consultation."""
    
    liste_resultats = charger_donnees(NOM_FICHIER)
    if liste_resultats is None or not liste_resultats:
        print("Chargement des données échoué ou fichier vide. Arrêt du programme.")
        return

    print(f"Données chargées avec succès depuis '{NOM_FICHIER}'.")

    while True:
        afficher_menu()
        choix = input("Votre choix: ")

        try:
            #  meilleur et le pire taux de réussite ?
            if choix == '1':
               
                
                meilleur = dnb.meilleur_taux_reussite(liste_resultats)
                pire = dnb.pire_taux_reussite(liste_resultats)
                
                print(f"Meilleur taux de réussite (global): {meilleur:.2f}%" if meilleur is not None else "Meilleur taux: N/A")
                print(f"Pire taux de réussite (global): {pire:.2f}%" if pire is not None else "Pire taux: N/A")
                

            # nb admis sessions
            elif choix == '2':
                try:
                    session = input("Entrez la session (année)? ")
                    session_num = int(session)
                except ValueError:
                    print("Erreur: Année invalide.")
                    continue 

                donnees_session = dnb.filtre_session(liste_resultats, session_num)
                totaux = dnb.total_admis_presents(donnees_session)
                if totaux and totaux[0] > 0:
                    print(f"Nombre total d'admis en {session_num}: {int(totaux[0])}")
                else:
                    print(f"Aucune donnée trouvée pour {session_num}.")

            # nb present pour departement+session
            elif choix == '3':
                try:
                    departement = input("Entrez un numéro de département? ")
                    dep_num = int(departement)
                    session = input("Entrez la session (année)? ")
                    session_num = int(session)
                except ValueError:
                    print("Erreur: Entrée invalide.")
                    continue

                donnees_session = dnb.filtre_session(liste_resultats, session_num)
                donnees_dep = dnb.filtre_departement(donnees_session, dep_num)
                totaux = dnb.total_admis_presents(donnees_dep)
                
                if totaux and totaux[1] > 0:
                    print(f"Nombre de présents : {int(totaux[1])}")
                else:
                    print(f"Aucune donnée trouvée pour le département {dep_num} en {session_num}.")
            #  taux de réussite d'un collège (session 2020)
            elif choix == '4':
                
                try:
                    dep_str = input("Entrez un numéro de département? ")
                    dep_num = int(dep_str)
                except ValueError:
                    print("Erreur: Numéro de département invalide.")
                    continue 

                nom_college = input("Entrez le nom du collège? ")
                session_num = 2020 

                donnees_session = dnb.filtre_session(liste_resultats, session_num)
                college_fonc = dnb.filtre_college(donnees_session, nom_college.upper(), dep_num)
                
                if college_fonc:
                    taux = dnb.taux_reussite(college_fonc[0])
                    if taux is not None:
                        print(f"Le taux de réussite pour le collège {college_fonc[0][1]} ({college_fonc[0][2]}) était de {taux:.1f}% pour la session {session_num} du DNB.")
                    else:
                        print("Calcul du taux impossible (nombre de présents nul).")
                else:
                    print(f"Collège '{nom_college}' ({dep_num}) non trouvé pour {session_num}.")

            # Meilleur college departement+session
            elif choix == '5':
                try:
                    dep_str = input("Entrez un numéro de département? ")
                    dep_num = int(dep_str)
                    session_str = input("Entrez la session (année)? ")
                    session_num = int(session_str)
                except ValueError:
                    print("Erreur: Entrée invalide.")
                    continue
                
                donnees_dep = dnb.filtre_departement(liste_resultats, dep_num)
                meilleur = dnb.meilleur_college(donnees_dep, session_num) 
                
                if meilleur:
                    print(f"Meilleur collège (Dép. {dep_num}, Session {session_num}): {meilleur[0]} ")
                else:
                    print(f"Impossible de déterminer le meilleur collège pour le département {dep_num} en {session_num}.")
            #  plus longue période d’amélioration  ?
            elif choix == '6':
                
                periode = dnb.plus_longe_periode_amelioration(liste_resultats)
                if periode:
                    print(f"Plus longue période d'amélioration nationale: de {periode[0]} à {periode[1]}")
                else:
                    print("Impossible de calculer la période d'amélioration.")
            # Quitter
            elif choix == '0':
                print("Au revoir !")
                break
            
            else:
                print("Choix invalide. Veuillez réessayer.")
        
        except Exception as e:
            print(f"Une erreur inattendue est survenue: {e}")
            print("Veuillez vérifier vos données ou les fonctions importées.")

# Point d'entrée 
if __name__ == "__main__":
    programme_principal()