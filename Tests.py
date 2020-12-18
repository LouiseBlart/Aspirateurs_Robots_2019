# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:45:52 2020

@author: Yvan Belakebi-Joly et Louise Blart
"""

from Deplacements import * 
import matplotlib.pyplot as plt
import pylab

def tester_e (n):
    '''
    Le paramétre e de la fonction deplacement_aletoire permet d'effectuer un
    deplacement vers l'avant avec probabilité e et de tourner avec probabilité
    1-e.
    Cette fonction permet de tester ce paramètre e afin de minimiser le nombre
    de déplacements et de rotations permettant le nettoyage total de la pièce.
    
    Exemple: 
        >>> tester_e(500)
            le e optimal est 0.7
    '''
    e=[x/10 for x in range(1,10,1)]
    liste=[]
    aspi = Aspirateur()
    for i in (e): # On teste tous les e de 0.1 à 1
        deplacement=[]
        rotation=[]
        for r in range (n):
            t=aspi.test_aleatoire(i)
            if x_longueur == aspi.long and x_largeur == aspi.larg : # On ne prend en compte seulement les nettoyages où l'intégralité de la pièce est nettoyée (pas toujours le cas puisque notre condition de fin n'est pas parfaite)
                deplacement.append(t[0])
                rotation.append(t[1])
            aspi = Aspirateur()
            matrice()
        # Le fait de se déplacer est plus couteux que de tourner ( explique le coefficient 1 devant le nombre de déplacements et le coefficient 0.5 pour le nombre de rotations)
        liste.append(int(np.mean(deplacement))+0.5*int(np.mean(rotation)))
    a=min(liste)
    print(liste)
    print('le e optimal est', (liste.index(a)+1)/10)   
    
def test_p (n):
    '''
    Le paramètre p de la fonction deplacement_aléatoire_ameliore permet 
    d'effectuer une rotation vers la droite avec probabilité p et vers la gauche
    avec probabilité 1-p.
    Cette fonction permet de tester le paramètre p de face a minimiser le nombre
    de déplacement total afin de nettoyer l'intégralité de la pièce avec 
    cette fonction deplacement_aléatoire_ameliore. 
    
    Exemple: 
        >>> test_p(500)
            le p optimal est 0.9
    '''
    aspi=Aspirateur()
    liste_tot =[]
    p=[x/10 for x in range(0,11,1)] # On teste tous les p de 0 à 10. 
    for m in p : 
        deplacement = []
        rotation =[]
        for i in range (n) :
            t=aspi.test_aleatoire_ameliore(m) 
            deplacement.append(t[0])
            rotation.append(t[1])
            aspi=Aspirateur()
            matrice()
            
        # Le fait de se déplacer est plus couteux que de tourner ( explique le coefficient 1 devant le nombre de déplacements et le coefficient 0.5 pour le nombre de rotations)
        liste_tot.append(int(np.mean(deplacement))+0.5*int(np.mean(rotation)) )
    a=min(liste_tot)
    print('le p optimal est ', (liste_tot.index(a))/10)
    return liste_tot





def test_efficacite_deplacements(n):
    '''
    Cette fonction teste l'efficacité de nos fonctions de déplacements pour une
    même pièce. Ce qui nous permettra ensuite de comparer nos fonctions.
    '''
    global pct_reussite_aleatoire, pct_reussite_ameliore
    aspi = Aspirateur()
    c=0
    d=0
    #e=0
    distrib_aleatoire = []
    distrib_ameliore=[]
    #distrib_dijkstra=[]
    
    for i in range(n):
        # Pour le déplacement aleatoire
        a=aspi.test_aleatoire ()
        if aspi.termine==True and x_largeur==aspi.larg and x_longueur==aspi.long:
            d+=1
            distrib_aleatoire.append(a[0])
        aspi = Aspirateur()
        matrice()
        
        # Pour le déplacement aleatoire ameliore
        t=aspi.test_aleatoire_ameliore ()
        if aspi.termine==True and x_largeur==aspi.larg and x_longueur==aspi.long:
            c+=1
            distrib_ameliore.append(t[0])
        aspi = Aspirateur()
        matrice()
        '''
        # Pour le deplacement avec dijkstra
        dij=aspi.test_ameliore_dijkstra ()

        if aspi.termine==True:
            e+=1
            distrib_dijkstra.append(dij[0])
        aspi = Aspirateur()
        matrice()
        '''
    pct_reussite_aleatoire= d/n * 100 
    pct_reussite_ameliore= c/n * 100
    #pct_reussite_dijkstra= e/n *100
    
    print ('le pourcentage de réussite des fonctions: \n aleatoire :',
           pct_reussite_aleatoire, '\n ameliore :', pct_reussite_ameliore)
    
    BoxName = ['aleatoire','ameliore']
    data = [distrib_aleatoire,distrib_ameliore]
    plt.boxplot(data)
    pylab.xticks([1,2], BoxName)
    plt.show()



"""
def test_efficacite_deplacement_aleatoire(n):
    '''
    Fonction qui montre que la fonction de déplacement n'est pas très efficace
    puisque dès que la pièce commence a grandire (plus de 7m sur 7m) ou quand 
    il y a beaucoup d'obstacles, l'aspirateur ne parvient pas à nettoyer la pièce 
    dans sa totalité.
    De plus, même pour des pièces moyennes, l'aspirateur va parfois croire à 
    tort que son travail est fini. La condition d'arret que nous avons élaboré
    n'est pas suffisante.
    '''
    aspi = Aspirateur()
    c=0
    for i in range(n):
        t=aspi.test_aleatoire_ameliore ()
        if x_longueur == aspi.long and x_largeur == aspi.larg :
            c+=1
        aspi = Aspirateur()
        matrice()
    return (c/n * 100 )
    
"""