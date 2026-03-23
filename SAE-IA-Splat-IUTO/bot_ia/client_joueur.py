# coding: utf-8
"""
Projet Splat'IUT'O

Licence pédagogique — usage académique uniquement                                                    
Copyright (c) 2026 Limet Sébastien / IUT'O, Université d'Orléans

Ce code est fourni exclusivement dans un cadre pédagogique.
Les étudiants sont autorisés à l’utiliser et le modifier uniquement
pour les besoins du projet évalué dans le cadre de la SAE1.02 du BUT Informatique d'Orléans.

Toute diffusion, publication ou réutilisation en dehors de ce cadre,
notamment sur des plateformes publiques, est interdite sans
autorisation écrite préalable de l’auteur.

Tous droits réservés.

Module contenant l'implémentation de l'IA et le programme principal du joueur
"""


import argparse
import random

from bot_ia  import client
from bot_ia  import const
from bot_ia  import plateau
from bot_ia  import case
from bot_ia  import joueur

INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0),
                 'O': (0, -1), 'X': (0, 0)}

def mon_IA(ma_couleur,carac_jeu, le_plateau, les_joueurs):
    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du joueur
        carac_jeu (dict)): un dictionnaire donnant les valeurs des caractéristiques du jeu:
             duree_actuelle, duree_totale, reserve_initiale, duree_obj, penalite, bonus_touche,
             bonus_recharge, bonus_objet et distance_max,
        le_plateau (dict): l'état du plateau actuel sous la forme décrite dans plateau.py
        les_joueurs (list[joueur]): la liste des joueurs avec leurs caractéristiques utilisant l'API
         joueur.py

    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement
    """
    # IA complètement aléatoire
    #return random.choice("XNSOE")+random.choice("NSEO")
    joueur_pos=joueur.get_pos(les_joueurs[ma_couleur])
    reservoir=joueur.get_reserve(les_joueurs[ma_couleur])
    differents_chemins=plateau.directions_possibles(le_plateau,joueur_pos)
    dico_objet_et_joueur_a_proximite=plateau.distances_objets_joueurs(le_plateau,joueur_pos,10)
    distances_triees = sorted(dico_objet_et_joueur_a_proximite.keys())
    #priorité 1: si un bidon est à proximité et le reservoir est négatif, aller le ramasser
    if reservoir<0:
        for dist in distances_triees:
            if const.BIDON in dico_objet_et_joueur_a_proximite[dist]:
                cible=get_case_bidon_a_proximite_plus_proche(le_plateau, joueur_pos, dist)
                if cible is not None:
                    case_prochain_deplacement=chemin_vers_cible(le_plateau,joueur_pos,cible)
                    direction_deplacement=case_prochain_deplacement[0]-joueur_pos[0],case_prochain_deplacement[1]-joueur_pos[1]
                    if direction_deplacement==(1,0):
                        return "X"+"S"
                    elif direction_deplacement==(-1,0):
                        return "X"+"N"
                    elif direction_deplacement==(0,1):
                        return "X"+"E"
                    elif direction_deplacement==(0,-1):
                        return "X"+"O"
    #priorité 2 : si une case est vide ou d'une autre couleur, la peindre et avancer
    for direction, couleur in differents_chemins.items():
        if couleur==' ' or couleur!=ma_couleur:
            return direction+direction
        elif couleur==ma_couleur:
            return random.choice("XNSOE")+random.choice("NSEO")



                


def chemin_vers_cible(plateau, pos_depart, pos_cible):
    if pos_depart==pos_cible:
        return pos_depart
    dejevisite={pos_depart}
    file_explo=[(pos_depart,[])]
    while file_explo!=[]:
        pos_actu,chemin=file_explo.pop(0)
        if pos_actu==pos_cible:
            return chemin[0]
        for x,y in INC_DIRECTION.values():
            voisin_pos=pos_actu[0]+x,pos_actu[1]+y
            if plateau.verification_dans_map(voisin_pos,plateau):
                case=plateau.get_case(plateau,voisin_pos)
                if case.est_mur(case)==False and voisin_pos not in dejevisite:
                    dejevisite.add(voisin_pos)
                    file_explo.append((voisin_pos,chemin+[voisin_pos]))
    return pos_depart







def get_case_bidon_a_proximite_plus_proche(le_plateau,pos_joueur,distance_max=10):
    """_summary_

    Args:
        plateau (_type_): _description_
        pos_joueur (_type_): _description_
        distance_max (int, optional): _description_. Defaults to 10.
    """
    adresse_debut=(pos_joueur[0]-distance_max, pos_joueur[1]-distance_max)
    adresse_fin=(pos_joueur[0]+distance_max, pos_joueur[1]+distance_max)
    liste_pos_BIDON_a_proxi=[]
    for lin in range(adresse_debut[0],adresse_fin[0]+1):
        for col in range(adresse_debut[1],adresse_fin[1]+1):
            if plateau.verification_dans_map((lin,col),le_plateau):
                if case.est_mur(plateau.get_case(le_plateau,(lin,col)))==False:
                    if case.get_objet(plateau.get_case(le_plateau,(lin,col)))==const.BIDON:
                        liste_pos_BIDON_a_proxi.append((lin,col))
    if liste_pos_BIDON_a_proxi==[]:
        return None
    return min(liste_pos_BIDON_a_proxi, key=lambda pos: abs(pos[0]-pos_joueur[0])+abs(pos[1]-pos_joueur[1]))




if __name__=="__main__":
    noms_caracteristiques=["duree_actuelle","duree_totale","reserve_initiale","duree_obj","penalite","bonus_touche",
            "bonus_recharge","bonus_objet","distance_max"]
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu=le_client.prochaine_commande()
        if ok:
            val_carac_jeu,etat_plateau,les_joueurs=le_jeu.split("--------------------\n")
            joueurs={}
            for ligne in les_joueurs[:-1].split('\n'):
                lejoueur=joueur.joueur_from_str(ligne)
                joueurs[joueur.get_couleur(lejoueur)]=lejoueur
            le_plateau=plateau.Plateau(etat_plateau)
            val_carac=val_carac_jeu.split(";")
            carac_jeu={}
            for i in range(len(noms_caracteristiques)):
                carac_jeu[noms_caracteristiques[i]]=int(val_carac[i])
    
            actions_joueur=mon_IA(id_joueur,carac_jeu,le_plateau,joueurs)
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")
