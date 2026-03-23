
# -----------------------------------------------------------------------------------------------------
# listes de fonctions à implémenter
# -----------------------------------------------------------------------------------------------------

def taux_reussite(resultat):
    """calcule le pourcentage de réussite correspondant au résultat

    Args:
        resultat (tuple): le résultat d'un collège pour une session (année)
        
    Returns:
        float:  le pourcentage de réussite (nb. admis / nb. présents ā la session)
    """
    if resultat[4]==0.0 and resultat[3]>0.0:
        return 0.0
    
    return  resultat[4]/resultat[3]*100 if  resultat[4]>0 and resultat[3]>0  else None


def meilleur(resultat1, resultat2):
    """vérifie si resultat1 est meilleur que resultat2 au sens des taux de réussites

    Args:
        resultat1 (tuple): un résultat d'un collège pour une session (année)
        resultat2 (tuple): un autre résultat d'un collège pour une session (année)

    Returns:
        bool:   True si le taux de réussite de resultat1 est supérieur ā celui de resultat2
    """  
    if taux_reussite(resultat1)== None:
        return False
    if taux_reussite(resultat2)== None:
        return True 
    if taux_reussite(resultat1)==None and taux_reussite(resultat2)==None:
        return False
    return taux_reussite(resultat1) >taux_reussite(resultat2) if taux_reussite(resultat1) != taux_reussite(resultat2) else False


def meilleur_taux_reussite(liste_resultats):
    """recherche le meilleur taux de réussite dans une liste de résultats

    Args:
        liste_resultats (list): une liste de resultats

    Returns:
        float: le meilleur taux de rēussite
    """
    if liste_resultats==[]:
        return None
    if len(liste_resultats)==1:
        return taux_reussite(liste_resultats[0])
    best=None
    for val in liste_resultats:
        if best == None or meilleur(val,best):
            best=val
    return taux_reussite(best) 



def pire_taux_reussite(liste_resultats):
    """recherche le pire taux de réussite parmi une liste de résultats

    Args:
        liste_resultats (list): une liste de resultats

    Returns:
        float: le pire taux de rēussite
    """
    if liste_resultats==[]:
        return None
    if len(liste_resultats)==1:
        return taux_reussite(liste_resultats[0])
    worst=0.0
    for val in liste_resultats:
        if worst == 0.0 or not meilleur(val,worst):
            worst=val
    return taux_reussite(worst)

def total_admis_presents(liste_resultats):
    """calcule le nombre total de candidats admis et de candidats présents aux épreuves du DNB parmi les résultats de la liste passée en paramètre

    Args:
        liste_resultats (list): une liste de résultats

    Returns:
        tuple : un couple d'entiers contenant le nombre total de candidats admis et prēsents
    """
    if liste_resultats==[]:
        return None
    if len(liste_resultats)==1:
        for i in liste_resultats:
            return (i[4],i[3])
    candidats_admis=0 
    candidats_presents=0

    for i in liste_resultats:
      candidats_admis = candidats_admis+ i[4]
      candidats_presents = candidats_presents+ i[3]
    return (candidats_admis, candidats_presents)


def filtre_session(liste_resultats, session):
    """génère la sous-liste de liste_resultats, restreinte aux résultats de la session demandée

    Args:
        liste_resultats (list): une liste de résultats
        session (int): une session (année)

    Returns:
        list: la sous-liste de liste_resultats, restreinte aux résultats de la session demandēe
    """
    
    filtre_ses=[]
    for i in range(len(liste_resultats)):
        if liste_resultats[i][0]==session:
            filtre_ses.append(liste_resultats[i])
    return filtre_ses


def filtre_departement(liste_resultats, departement):
    """génère la sous-liste de liste_resultats, restreinte aux résultats du département demandé

    Args:
        liste_resultats (list): une liste de résultats
        departement (int): un numéro de département

    Returns:
        list: la sous-liste de liste_resultats, restreinte aux résultats du dēpartement demandé
    """
    
    filtre_dep=[]
    for i in range(len(liste_resultats)):
        if liste_resultats[i][2]==departement:
            if liste_resultats[i][2]>0:
                filtre_dep.append(liste_resultats[i])
    return filtre_dep


def filtre_college(liste_resultats, nom, departement):
    """génère la sous-liste de liste_resultats, restreinte aux résultats du département donné et dont le nom du collège contient le nom passé en paramètre (en minuscule ou majuscule)

    Args:
        liste_resultats (list): une liste de résultats
        nom (str): un nom de collège (éventuellement incomplet)
        departement (int) : un numéro de département

    Returns:
        list: la sous-liste de liste_resultats, restreinte aux résultats du collège et du département recherchēs
    """
    
    nom=nom.lower()
    filtre_col=[]
    for i in range(len(liste_resultats)):
        if nom in liste_resultats[i][1].lower() and liste_resultats[i][2]==departement:
            filtre_col.append(liste_resultats[i])
    return filtre_col


def taux_reussite_global(liste_resultats, session):
    """calcule le taux (pourcentage) de réussite au DNB sur l'ensemble des collèges pour une session donnée

    Args:
        liste_resultats (list): une liste de résultats
        session (int) : une session (année)
        
    Returns:
        float: taux (pourcentage) de réussite au DNB sur l'ensemble des collèges pour une session donnēes
    """
    if liste_resultats == []:
        return None

    
    resultats_session = []
    for i in liste_resultats:
        if i[0] == session:
            resultats_session.append(i)

    if resultats_session == []:
        return None

    
    admis, presents = total_admis_presents(resultats_session)

    
    if presents == 0:
        return None

    
    return (admis / presents) * 100
            
        



def moyenne_taux_reussite_college(liste_resultats, nom, departement):
    """calcule la moyenne des taux de réussite d'un collège sur l'ensemble des sessions

    Args:
        liste_resultats (list): une liste de résultats
        nom (str): un nom de collège (exact)
        departement (int) : un numéro de département
        
    Returns:
        float: moyenne des taux de rēussite d'un collège sur l'ensemble des sessions
    """
    if liste_resultats == []:
        return None
    somme=0
    liste_moy=[]
    for i in liste_resultats:
        if i[1] == nom and i[2]==departement:
            if taux_reussite(i) != None:
                somme=somme + taux_reussite(i)
                liste_moy.append(i) 
    if len(liste_moy)==0:
            return None
    return somme/len(liste_moy)
    

        




def meilleur_college(liste_resultats, session):
    """recherche le collège ayant obtenu le meilleur taux de réussite pour une session donnée

    Args:
        liste_resultats (list): une liste de résultats
        session (int) : une session (année)
        
    Returns:
        tuple: couple contenant le nom du collège et le dēpartement
    """
    if liste_resultats == []:
        return None
    liste_session=[]
    for i in liste_resultats:
        if i[0]==session:
            liste_session.append(i)
    best=meilleur_taux_reussite(liste_session)
    for i in liste_session:
        if best != None and taux_reussite(i) !=None:
            if best==taux_reussite(i):
                return (i[1],i[2])
    return None


            
            

    


def liste_sessions(liste_resultats):
    """retourne la liste des sessions (années) dont au moins un résultat est reporté dans la liste de résultats.
    ATTENTION : la liste renvoyée doit être sans doublons et triée par ordre chronologique des sessions 

    Args:
        liste_resultats (list): une liste de résultats

    Returns:
        list: une liste de session (int) triēe et sans doublons
    """    
    if liste_resultats == []:
        return []
    liste_nb_session=[]
    for i in liste_resultats:
        if i[0] not in liste_nb_session :
            liste_nb_session.append(i[0])
    return liste_nb_session



def plus_longe_periode_amelioration(liste_resultats):
    """recherche la plus longue periode d'amélioration du taux de réussite global au DNB

    Args:
        liste_resultats (list): une liste de résultats

    Returns:
        tuple: un couple contenant la session (année) de début de la période et la session de fin de la pēriode
    """   
    
    sessions = liste_sessions(liste_resultats)
    

    
    if liste_resultats == []:
        return None
    if len(sessions) ==1:
        return (sessions[0], sessions[0]) 

    
    meilleure_periode = (sessions[0], sessions[0])
    debut_actuel = sessions[0]

    
    for i in range(1, len(sessions)):
        taux_precedent = taux_reussite_global(liste_resultats, sessions[i-1])
        taux_actuel = taux_reussite_global(liste_resultats, sessions[i])

        
        if not (taux_actuel and taux_precedent and taux_actuel > taux_precedent):
            if (sessions[i-1] - debut_actuel) > (meilleure_periode[1] - meilleure_periode[0]):
                meilleure_periode = (debut_actuel, sessions[i-1])
            
            debut_actuel = sessions[i]

    
    if (sessions[-1] - debut_actuel) > (meilleure_periode[1] - meilleure_periode[0]):
        meilleure_periode = (debut_actuel, sessions[-1])
        
    return meilleure_periode
    


def est_bien_triee(liste_resultats):
    """vérifie qu'une liste de résultats est bien triée dans l'ordre chronologique des sessions puis dans l'ordre croissant des départements puis dans l'ordre alphabétique des noms de collèges
    
    Args:
        liste_resultats (list): une liste de résultats

    Returns:
        bool: True si la liste est bien triēe et False sinon
    """
    if liste_resultats == []:
        return True
    
    trie_session=True
    trie_departements=True
    trie_college=True

    sessions = liste_sessions(liste_resultats)
    for i in range(len(sessions)-1):
        if len(sessions) !=1:
            if sessions[i]>sessions[i+1]:
                trie_session=False
            else: 
                trie_session=True
        
    for i in range(len(liste_resultats)-1):
        if len(liste_resultats) !=1:
            if liste_resultats[i][2]>liste_resultats[i+1][2]:
                trie_departements=False
            else: trie_departements=True

    for i in range(len(liste_resultats)-1):
        if len(liste_resultats) !=1:
            if liste_resultats[i][1][0]>liste_resultats[i+1][1][0]:
                trie_college=False
            else: trie_college=True


    
    return trie_session and trie_departements and trie_college
    
            





def fusionner_resultats(liste_resultats1, liste_resultats2):
    
    """Fusionne deux listes de résultats triées sans doublons en une liste triée sans doublon
    sachant qu'un même résultat peut être présent dans les deux listes

    Args:
        liste_resultat1 (list): la première liste de résultats
        liste_resultat2 (list): la seconde liste de résultats

    Returns:
        list: la liste triée sans doublon comportant tous les rēsultats
                de liste_resultats1 et liste_resultats2
    """
    res = []
    ind1 = 0  
    ind2 = 0  

    
    while ind1 < len(liste_resultats1) and ind2 < len(liste_resultats2):
       
        if liste_resultats1[ind1] <= liste_resultats2[ind2]:
            element = liste_resultats1[ind1]
            if not res or res[-1] != element:
                res.append(element)
                ind1 += 1
        elif liste_resultats1[ind1] == liste_resultats2[ind2]:
                    ind2+=1                
        
        else:
            element = liste_resultats2[ind2]
            if not res or res[-1] != element:
                res.append(element)
            ind2 += 1

    
    while ind1 < len(liste_resultats1):
        element = liste_resultats1[ind1]
        if not res or res[-1] != element:
            res.append(element)
        ind1 += 1

   
    while ind2 < len(liste_resultats2):
        element = liste_resultats2[ind2]
        if not res or res[-1] != element:
            res.append(element)
        ind2 += 1

    return res


def charger_resultats(nom_fichier):
    """charge un fichier de résultats au DNB donné au format CSV en une liste de résultats

    Args:
        nom_fichier (str): nom du fichier CSV contenant les résultats au DNB

    Returns:
        list: la liste des rēsultats contenus dans le fichier
    """
    res = []
    with open(nom_fichier, 'r') as fic:
        fic.readline() 
        for ligne in fic:
            l_champs = ligne.strip().split(",")
            
            res.append((int(l_champs[0]), (l_champs[1]), int(l_champs[2]), int(l_champs[3]), int(l_champs[4])))
    return res
                





