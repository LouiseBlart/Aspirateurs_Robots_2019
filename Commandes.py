# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:16:44 2020

@author: Yvan Belakebi-Joly et Louise Blart
"""

"""
Ce fichier comprend les différentes commandes utilisées pour l'élaboration
de notre projet. Ce sont les commandes plus ou moins annexes de notre aspirateur.
Ce fichier n'est pas à executer seul mais sera utile dans le fichier Deplacements.

"""

from random import random
def OnValidate(S):
    '''
    Cette fonction permet de tester le paramètre S. 
    Elle renvera True si celui-ci est bien un nombre décimal strictement 
    positif et False dans le cas contraire
    
    Exemples :
        >>> OnValidate('6')
            True
        >>> OnValidate('a')
            False
    '''
    if (S.isdigit(),S > '0')== (True,True):
        return True
    return False


def IsIn (L,l):
    '''
    Cette fonction prend en paramétre deux listes.
    Elle teste si la liste l est incluse dans la liste L. 
    
    Exemple : 
        >>> L = [[350, 250], [350, 350], [250, 350], [250, 450], [450, 450]]
        >>> l = [350, 350]
        >>> IsIn (L,l)
            True
    '''
    rep = False 
    for i in L :
        if l == i : 
            rep = True 
    return rep 


def addition (X,Y):
    """
    Fonction permettant d'additionner des coordonnées.
    Elle sera utile pour permettre le déplacement de notre aspirateur
    
    Elle prend en argument deux listes de longueur deux.
    
    Exemple: 
        >>> addition([1,1],[0,1])
        [1, 2]
    """
    Z = [X[0]+Y[0],X[1]+Y[1]]
    return Z 

def Case_dans_Matrice (Case,Matrice):
    """
    Cette fonction renvoie la valeur de la matrice "Matrice" aux coordonnées 
    de la case "Case"
    Exemple : 
        >>> M=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        >>> Case = [0,1]
        >>> Case_dans_Matrice (Case,M)
            2
    
    """
    a= Matrice[Case[0],Case[1]]
    return a 

def Bernoulli (p,a,b):
    """
    Cette fonction renvoie a avec probabilité p et b avec probabilité 1-p
    
    Exemple: 
        >>> Bernoulli(0.5,[-1,1],[1,1])
            [1, 1]
    """
    return a if random() < p else b

def Nouvelle_case_face (position, case_face,p):
    """
    Cette fonction renvoie la case en face de l'apisateur 
    s'il effectue avec probabilité p une rotation vers la droite
    et p-1 pour une rotation vers la gauche
    """
    if position[0] == case_face[0]: # L'aspirateur et la case en face sont sur la même ligne
        if position[1] < case_face[1] : # Si on regarde la case à droite de l'aspirateur
            a= Bernoulli(p,[1,-1],[-1,-1]) # Alors on va se tourner vers la case du bas avec probabilité p et la case du haut avec probabilité 1-P
        else : # On regarde la case à gauche de l'aspirateur
            a=Bernoulli(p,[-1,1],[1,1]) # on se tourne pour regarder la case du dessus avec probabilité p ou la case du dessous avec probabilité 1-P
    elif position[0] > case_face[0]: # La case en face est au dessus de l'aspirateur
        a=Bernoulli(p,[1,1],[1,-1]) # rotation vers la droite avec probabilité p, vers la gauche avec probabilité 1-P
    else : # La case en face est en dessous
        a=Bernoulli(p,[-1,-1],[-1,1]) # rotation vers la droite avec probabilité p, vers la gauche avec probabilité 1-P
    return a 

def ajout_sans_doublon (c,L) :
    """ 
    cette fonction ajoute c à la liste l s'il n'est pas deja inclus
    dans cette liste
    """
    if IsIn(L,c) == False :
        L.append(c)
    return L   

def transformerentuple(couple):
    return(couple[0],couple[1])