# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:57:50 2020

@author: Yvan Belakebi-Joly et Louise Blart
"""
"""
Ce fichier contient les différentes fonction permettant à l'aspirateur de se déplacer
Ici, nous nous interessons à la programmation d'un aspirateur robot ayant un seul
capteur sur l'avant (lui permettant d'identifier la case devant lui seulement),
et qui ne peut effectuer seulement deux opérations (sans compter le nettoyage) : 
    - effectuer une rotation
    - se déplacer d'une case en avant. 
Nous allons nous interesser à la programmation de cet aspirateur robot ; 
comment nettoyer une pièce le plus rapidement possible en évitant les objets.

C'est ce fichier déplacement qui est a effectuer (il prend en compte les autres 
fichiers)
"""

from Interface_Graphique import *
from Commandes import * 
import numpy as np
from math import *
from queue import *



'''
# Nous permet de réaliser plus rapidement nos déplacement sans devoir réactualiser à chaque fois l'interface graphique
x_longueur=5
x_largeur=5
x_case=100
liste_objet=[ [150,250], [150, 150], [150, 50], [250, 450], [350, 350]]
depart_aspirateur=[[50, 50]]
'''

longueur=x_longueur
largeur=x_largeur
   
def matrice ():
    '''
    Cette fonction nous permet, à partir des données inséré par l'utilisateur
    dans l'interface graphique, de convertir la piece en matrice. 
    On ajoute egalement des murs autour de la pièce représentés par un 1. 
    Notation : 
        - 0 : case vide non nettoyée
        - 1 : obstacle 
        - 3 : case nettoyée
        - 4 : position de l'aspirateur
        - 5 : position de depart de l'aspirateur
    '''
    global M,depart,liste_coordonnée,obstacles # Nous permet de les réutiliser par la suite
    obstacles=[]
    M=np.zeros((x_longueur+2,x_largeur+2)) # +2 car on ajoute des murs tout autour 
    liste_coordonnée=[]
    for i in range (x_longueur+2):
        for j in range(x_largeur+2):
            if i==0 or j ==0 or i==x_longueur+1 or j==x_largeur+1: # On crée les murs de la piece
                    M[i,j]= 1    
            else:
                liste_coordonnée.append([i,j])
                if IsIn(liste_objet,[int(x_case/2 + (i-1)*x_case), int(x_case/2 + (j-1)*x_case)]): # Si la case est dans la liste des objets
                    obstacles.append([i,j]) # On ajoute cet obstacle a la liste des obstacles
                    M[i,j]=1
                elif IsIn(depart_aspirateur,[int(x_case/2 + (i-1)*x_case), int(x_case/2 + (j-1)*x_case)]):
                    M[i,j]=4 # Le chiffre 4 représente la position de l'aspirateur
                    depart= [i,j]
matrice()

def rotations_chemin(chemin):
    cpt=0
    c=0
    d=0
    if len(chemin)==1:  
        return cpt
    if chemin[1][0]!=chemin[0][0]:
        c=1
        d=1
    for k in range(2,len(chemin)):
        if chemin[k][0]==chemin[k-1][0]:
            c=0
            if d!=c:
                cpt+=1
        else:
            c=1
            if d!=c:
                cpt+=1
        d=c
    return cpt

class Aspirateur ():
    def __init__(self):
        '''
        Cette classe permet de stocker les caractéristiques de l'aspirateur. 
        Ils évoluent en fonction des déplacements.
        '''
        self.position = depart
        self.case_face= addition(self.position,[1,0]) # La case en face de notre aspirateur (l'aspirateur a seulement des capteurs à l'avant)
        self.nb_deplacements = 0 
        self.nb_rotation = 0
        self.cases_nettoyées = []
        self.obstacles = []
        self.long= 1 # longueur de la piece initialement connue par l'aspirateur (1 car l'utilisateur est contraint d'entrer des entiers strictement supérieurs à 0 pour les dimensions de la pièce)
        self.larg= 1 # largeur de la piece initialement connue par l'aspirateur
        self.termine = False
    
    def cartographier(self,case_face) :
        '''
        Cette fonction permet à l'aspirateur de cartographier la piece 
        afin de connaitre les dimensions exacte de la pièce (permet de mettre
        en place une condition d'arret quand l'aspirateur a nettoyé toute la 
        pièce).
        En effet l'aspirateur ne connait ni la longueur ni la largeur de la 
        piece qu'il explore, il va donc essayer de la connaitre au fur et à 
        mesure où il se déplace dans celle-ci.
        '''
        if self.long< case_face[0]-1 : # Si la case sur laquelle l'aspirateur se trouve a une longueur supérieure à celle que nous avions juqu'à présent pour la pièce
            self.long = case_face[0]-1 # alors la longueur de la pièce prend cette valeur
        if self.larg< case_face[1]-1 : # De la même manière pour la largeur
            self.larg = case_face[1]-1
    
    
    def deplacement_aleatoire (self,e = 0.7) :
        '''
        Cette fonction est la première fonction de déplacement que nous étudions.
        Elle permet a l'aspirateur de :
            - Essayer d'avancer avec probabilité e
            - Effectuer une rotation avec probabilité 1-e.
        La valeur qui minimise le nombre de rotations et de déplacements est 
        de e= 0.7 (voir le fichier Test.py où nous testons les paramètres de nos
        fonctions pour les rendre optimales). C'est pourquoi, nous fixons la 
        valeure par défaut de e à 0.7.
        ( L'aspirateur va donc plus souvent tenter d'avancer que de tourner.)
        '''
        p = random() # Notre paramétre aléatoire
        self.cartographier (self.case_face ) # On regarde si on ne peut pas augmenter la largeur et la longueur connue par l'aspirateur
        if Case_dans_Matrice(self.case_face,M) == 3 : # Si devant nous on observe une case déja nettoyée c'est peut être que l'aspirateur a terminé son travail
            self.fin() # On vérifie 
        if p < e: # Si p est inférieur à e 
            if Case_dans_Matrice(self.case_face,M)!=1: # S'il n'y a pas d'obstacle à l'avant
                self.nb_deplacements+=1 # Peut avancer donc le nombre de déplacmenet augmente de 1
                if self.position == depart : 
                    M[self.position[0],self.position[1]] = 5 # Pour toujours repérer la case de départ
                else :
                    M[self.position[0],self.position[1]] = 3 # On indique que la case est nettoyée
                self.cases_nettoyées =ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées) # On enregistre les cases que l'on a déjà nettoyée
                a=[self.case_face[0]-self.position[0] ,self.case_face[1]-self.position[1]] # va nous permettre d'avancer ensuite sur la case souhaitée
                self.position = self.case_face # L'aspirateur se déplace sur la case vide 
                self.case_face = addition(self.case_face,a) # on actualise la case en face
                M[self.position[0],self.position[1]] = 4 # On actualise la position de l'aspirateur
                #print(M)
            else : # On est en présence d'un obstacle
                if self.case_face[0] != 0 and  self.case_face[0] != self.long +1 and self.case_face[1] != self.larg +1 and self.case_face[1] != 0:
                    self.obstacles = ajout_sans_doublon ([self.case_face[0],self.case_face[1]],self.obstacles) # On actualise la liste des objets seulement si ce n'est pas un mur
                self.deplacement_aleatoire(e) # On relance la fonction déplacement
                
        else : # Avec probabilité 1-e on effectue une roation
            self.nb_rotation += 1
            a= Nouvelle_case_face (self.position, self.case_face,0.5) # On actualise la case en face, rotation à droite ou à gauche avec probabilité 0.5. 
            self.case_face = addition(self.case_face,a)
        #print(M)

        
    def deplacement_aleatoire_ameliore (self,p) :
        '''
        Cette deuxieme fonction de déplacement est plus efficace que la première
        puisque cette fonction analyse d'abord ce qu'il y a devant l'aspirateur
        avant de choisir d'effectue une rotation ou un déplacement vers l'avant. 
        '''
        if Case_dans_Matrice (self.case_face,M) == 0:  # La case en face est libre, on avance
            self.nb_deplacements += 1 # Le nombre de déplacements augmente de 1
            if self.position == depart : 
                M[self.position[0],self.position[1]] = 5 # représente le socle de rechargement
                self.cases_nettoyées =ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées)
            else :
                M[self.position[0],self.position[1]] = 3 # La case a été nettoyée par l'aspirateur
                self.cases_nettoyées = ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées)
            a=[self.case_face[0]-self.position[0] ,self.case_face[1]-self.position[1]] # Va nous permettre d'avancer
            self.position = self.case_face # L'aspirateur se déplace sur la case vide 
            self.case_face = addition(self.case_face,a) # On actualise la case en face
            M[self.position[0],self.position[1]] = 4 # On actualise la position de l'aspirateur
            #print(M)            
        
        elif Case_dans_Matrice (self.case_face,M) == 1 : # Si on est face a un objet
            # cartographier la pièce : 
            self.cartographier(self.case_face)
            if self.case_face[0] != 0 and  self.case_face[0] != self.long +1 and self.case_face[1] != self.larg +1 and self.case_face[1] != 0:
                self.obstacles = ajout_sans_doublon ([self.case_face[0],self.case_face[1]],self.obstacles) # Actualiser la liste des objets si ce n'est pas un mur
                
            # Permet l'évolution de l'aspirateur : 
            self.nb_rotation += 1 # On est face a un objet donc on tourne
            a= Nouvelle_case_face (self.position, self.case_face,p)
            self.case_face = addition(self.case_face,a) # On actualise la case de face
            self.deplacement_aleatoire_ameliore(p) # On relance la fonction 
       
        else : # L'aspirateur est déja passé sur la case en face de nous
            # On regarde les cases autours, y a-t-il des cases encore sales ? :
            for i in range(4): 
                self.nb_rotation += 1
                a= Nouvelle_case_face (self.position, self.case_face,p)
                self.case_face = addition(self.case_face,a)
                # Cartographier : 
                if Case_dans_Matrice (self.case_face,M) == 1 and self.case_face[0] != 0 and  self.case_face[0] != self.long +1 and self.case_face[1] != self.larg +1 and self.case_face[1] != 0:
                    self.obstacles = ajout_sans_doublon ([self.case_face[0],self.case_face[1]],self.obstacles) # Actualise la liste des objets
                # Retour au déplacement
                if Case_dans_Matrice (self.case_face,M) == 0 : # On trouve une case vide autour de l'aspirateur, on avance de ce coté
                    return self.deplacement_aleatoire_ameliore(p)
            # Si on arrive a ce stage, l'aspirateur est entouré de case déja nettoyées ou d'obstacles, on cherche donc à revenir sur nos pas et donc repasser sur une case déja nettoyée
            while Case_dans_Matrice (self.case_face,M) !=3 : # On ne peut que se déplacer sur une case déja nettoyée
                a= Nouvelle_case_face (self.position, self.case_face,p) # On actualise
                self.case_face = addition(self.case_face,a)
            a=[self.case_face[0]-self.position[0] ,self.case_face[1]-self.position[1]]
            M[self.position[0],self.position[1]] = 3
            self.cases_nettoyées =ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées)
            self.position = self.case_face # L'aspirateur se déplace sur la case disponible 
            self.case_face = addition(self.case_face,a)
            M[self.position[0],self.position[1]] = 4
            self.nb_deplacements += 1
            self.fin() # On repasse sur une case déja nettoyée, c'est peut être que la pièce est entièrement nettoyée, on vérifie le test de fin.
        #print(M)
    

    def fin (self):
        '''
        Cette fonction permet de tester si notre aspirateur a entièrement 
        nettoyée la pièce. 
        La pièce est nettoyée si la multiplication de la largeur et de la longueur
        trouvées est égale à le nombre de cases explorées (nettoyées ou obstacles). 
        Cette condition de fin n'est pas parfaite puisqu'il est possible par 
        hasard que cette condition soit satisfaite sans que l'aspirateur ait 
        terminé son travail.
        '''
        if self.long*self.larg == len(self.cases_nettoyées) + len(self.obstacles) : # nombre de cases explorées = dimensions trouvées pour la pièce
            self.termine = True 

    def test_aleatoire(self,e=0.7,Iter=x_longueur*x_largeur*10):
        '''
        Cette fonction retourne le nombre de déplacements et de rotations 
        necessaires pour nettoyer entièrement la pièce avec la fonction de
        déplacement déplacement_aleatoire.
        On fixe le paramétre p = 1 par défaut car c'est la valeur de p qui
        minimise le nombre de déplacements et de rotations à effectuer 
        (cf le fichier Tests.py)
        
        Exemple: 
            >>> Robot = Aspirateur()
            >>> Robot.test_aleatoire()
                [91, 130]
                Il faut donct 76 déplacements et 235 rotations pour nettoyer 
                cette pièce.
        '''
        i=0

        while self.termine != True and i<Iter:
            self.deplacement_aleatoire(e)
            #print(M)
            i+=1
        if i>=Iter:
            print("Le nombre d'itération est maximal")
        return[self.nb_deplacements, self.nb_rotation]
    
    def test_aleatoire_ameliore (self,p=0.9,Iter=x_longueur*x_largeur*10):
        '''
        Cette fonction retourne le nombre de déplacements et de rotations 
        necessaires pour nettoyer entièrement la pièce avec la fonction de
        déplacement deplacement_aleatoire_ameliore.
        On fixe le paramétre p = 1 par défaut car c'est la valeur de p qui
        minimise le nombre de déplacements et de rotations à effectuer 
        (cf le fichier Tests.py)
        
        Exemple: 
            >>> Robot = Aspirateur()
            >>> Robot.test_aleatoire_ameliore()
                [32, 61]
                Il faut donct 76 déplacements et 235 rotations pour nettoyer 
                cette pièce.
        '''
        i=0
        while self.termine != True and i<Iter : 
            self.deplacement_aleatoire_ameliore(p)
            i+=1
        if i>=Iter:
            
            print("Le nombre d'itération est maximal")
        return[ self.nb_deplacements, self.nb_rotation]
      
    def test_ameliore_dijkstra (self,p=0.9):
        '''
        Cette fonction retourne le nombre de déplacements et de rotations 
        necessaires pour nettoyer entièrement la pièce avec la fonction de
        déplacement deplacement_aleatoire_ameliore.
        On fixe le paramétre p = 1 par défaut car c'est la valeur de p qui
        minimise le nombre de déplacements et de rotations à effectuer 
        (cf le fichier Tests.py)
        
        Exemple: 
            >>> Robot = Aspirateur()
            >>> Robot.test_aleatoire_ameliore()
                [32, 61]
                Il faut donct 76 déplacements et 235 rotations pour nettoyer 
                cette pièce.
        '''
        taille= int(0.9*(x_longueur*x_largeur))
        while taille > len(self.cases_nettoyées) + len(self.obstacles):
            self.deplacement_aleatoire_ameliore(p)
        print(M)
        self.relier_dijkstra ()


    def matrice_adjacente(self):
        adj=inf*np.ones((longueur+2,largeur+2,longueur+2,largeur+2))
        for i in range(1,longueur+1):
            for j in range(1,largeur+1):
                adj[i,j,i,j]=0
                if i!=1 and [i,j] not in self.obstacles and [i-1,j] not in self.obstacles:
                    adj[i,j,i-1,j]=1
                    adj[i-1,j,i,j]=1
                if i!=longueur and [i,j] not in self.obstacles and [i+1,j] not in self.obstacles:
                    adj[i,j,i+1,j]=1
                    adj[i+1,j,i,j]=1
                if j!=1 and [i,j] not in self.obstacles and [i,j-1] not in self.obstacles:
                    adj[i,j,i,j-1]=1
                    adj[i,j-1,i,j]=1
                if j!=largeur and [i,j] not in self.obstacles and [i,j+1] not in self.obstacles:
                    adj[i,j,i,j+1]=1
                    adj[i,j+1,i,j]=1
        return adj
    
    
    
    def dijkstra(self, but): #but: déterminer si une case est accessible et trouver le chemin le plus rapide
    
        #t1=time.clock()
        graphe=self.matrice_adjacente() #ce n'est pas vraiment un graphe, simplement une matrice utilisée comme un graphe
    
        file_attente=PriorityQueue()  #queue dont l'ordre de priorité est la distance à la position initiale
        
        position=transformerentuple(self.position)
        print("position",position )
        file_attente.put((self.position, 0))  #initialisation
        dict_distance_min = {position: 0}  #dictionnaire contenant la distance de chaque case du cadrillage à la self.position initiale
    
        dict_chemin_parcouru ={position: self.position} #dictionnaire contenant le chemin correspondant à cette distance
        
        while True:
            if file_attente.empty():
                break
            entree=file_attente.get()  #get retire l'objet de la queue
            distance,noeud = entree
            noeudt=transformerentuple(noeud)
            print (file_attente)

            if noeud[0]>=1 and noeud[1]>=1 and noeud[0]<=longueur and noeud[1]<=largeur:
                for couple in [[noeud[0]-1,noeud[1]],[noeud[0]+1,noeud[1]],[noeud[0],noeud[1]+1],[noeud[0],noeud[1]-1]]:
                    #if couple not in self.obstacles:
                    i,j=couple
                    couplet=transformerentuple(couple)
                    nouvelle_distance=distance+ graphe[noeud[0],noeud[1],i,j]
                    distance_minimale=dict_distance_min.get(couplet)
                    if (distance_minimale is None or nouvelle_distance<=distance_minimale):
                        dict_distance_min[couplet]=nouvelle_distance
                        plus_court_chemin=dict_chemin_parcouru[noeudt]
                        dict_chemin_parcouru[couplet]=plus_court_chemin+[couple]
                        file_attente.put((nouvelle_distance,couple))
                        
        butt=transformerentuple
        distance=dict_distance_min[butt]
        chemin=dict_chemin_parcouru[butt]
       # if distance is None :
        #    self.obstacles.append(but)
        if not isinf(distance):
            return floor(distance), chemin
            print(distance)
        else:
            self.obstacles.append(but)
        #t2=time.clock()
        #print(t2-t1)
    
    #le chemin parcouru l'est dans la matrice adjacente, donc les murs sont en 0 et longueur+2
    #et tout est décalé d'un indice
    #esquive les obstacles tant qu'il ne faut pas faire demi-tour (sans doute problème de comparaison de distance avec +inf)
    
    def suivre_chemin(self,chemin):
        for k in range(len(chemin)):
            couple=chemin[k]
            if couple in obstacles:
                self.obstacles=ajout_sans_doublon(couple, self.obstacles)
                return False
            else:
                self.position=couple
                self.nb_deplacements+=1
                self.cases_nettoyées=ajout_sans_doublon(couple, self.cases_nettoyées)
        return True

    
    
    def relier_dijkstra(self):  #sans réellement optimiser
        test=False
        à_nettoyer=[]
        for i in range(1, longueur+1):
            for j in range(1, largeur+1):
                if (([i,j] not in self.obstacles) and ([i,j] not in self.cases_nettoyées) and ([i,j]!=depart)):
                    à_nettoyer.append([i,j])
        à_nettoyer.sort()
        while len(à_nettoyer)!=0:
            print(à_nettoyer)
            distance, chemin=self.dijkstra(à_nettoyer[0])
            if distance is not None:
                test=self.suivre_chemin(chemin)
                self.nb_rotation+= rotations_chemin(chemin)
            if test:
                à_nettoyer.remove(à_nettoyer[0])
            print(test)
            
        if depart in self.obstacles: 
            (self.obstacles).remove(depart)
        '''
        retour=self.dijkstra(depart)[1]
        self.suivre_chemin(retour)
        self.nb_rotation+=rotations_chemin(retour)
        '''
        for i in range(1,longueur+1):
            for j in range(1,largeur+1):
                if [i,j]==depart:
                    M[i,j]=5
                elif [i,j]==self.position:
                    M[i,j]=4
                elif [i,j] in self.obstacles:
                    M[i,j]=1
                elif [i,j] in self.cases_nettoyées:
                    M[i,j]=3
        print(M)
    
    # def relier_dijkstra_cher(self):  faire un dijkstra avec les distances calculées par le premier dijkstra sûrement pas opti
    
       
    
'''
    def warshall_floyd(self):
        W=matrice_adjacente(self.obstacles)
        D=[]
        E=[]
        F=[]
        G=[]
        for a in range(longueur+2):
            D.append(E)
            for b in range(largeur+2):
                E.append(F)
                for c in range(longueur+2):
                    F.append(G)
                    for d in range(largeur+2):
                        G.append([(c,d)])
        for g in range(1, longueur+1):
            for h in range(1, largeur+1):
                for i in range(1, longueur+1):
                    for j in range(1, largeur+1):
                        for k in range(1, longueur+1):
                            for l in range(1, largeur+1):
                                if W[i,j,g,h]+W[g,h,k,l]<W[i,j,k,l]:
                                    D[i,j,k,l]=D[i,j,g,h]
        return W,D
    
    def recuperer_chemin_warshall(D, départ, arrivée):
        chemin=[]
        successeur= D[départ[0],départ[1], arrivée[0],arrivée[1]]
        if successeur== arrivée:
            chemin.append(arrivée)
            return chemin
        else:
            chemin.append(successeur)
            return recuperer_chemin_warshall(D,successeur,arrivée)
    
    
    
    def relier_Warshall(self):
        W,D=warshall_floyd(self)
        à_nettoyer=[]
        for i in range(1, longueur+1):
            for j in range(1, largeur+1):
                if (i,j) not in self.obstacles and (i,j) not in self.cases_nettoyées:
                    à_nettoyer.append((i,j))
        while len(à_nettoyer)!=0:
            m=à_nettoyer.index(min(à_nettoyer[k][0]+à_nettoyer[k][1]) for k in range(len(à_nettoyer)))
            chemin=recuperer_chemin_warshall(warshall_floyd(self),self.position,à_nettoyer[m])
            suivre_chemin(self,chemin)
            self.nb_rotation+= rotations_chemin(chemin)
            à_nettoyer.remove(à_nettoyer[m])
        retour=recuperer_chemin_warshall(warshall_floyd(self),self.position,départ)
        suivre_chemin(self, retour)
        self.nb_rotation+=rotations_chemin(retour)





    def deplacement_aleatoire_ameliore (self,p) :
        
        Cette deuxieme fonction de déplacement est plus efficace que la première
        puisque cette fonction analyse d'abord ce qu'il y a devant l'aspirateur
        avant de choisir d'effectue une rotation ou un déplacement vers l'avant. 
        
        if Case_dans_Matrice (self.case_face,M) == 0:  # La case en face est libre, on avance
            self.nb_deplacements += 1 # Le nombre de déplacements augmente de 1
            if self.position == depart : 
                M[self.position[0],self.position[1]] = 5 # représente le socle de rechargement
                self.cases_nettoyées =ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées)
            else :
                M[self.position[0],self.position[1]] = 3 # La case a été nettoyée par l'aspirateur
                self.cases_nettoyées = ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées)
            a=[self.case_face[0]-self.position[0] ,self.case_face[1]-self.position[1]] # Va nous permettre d'avancer
            self.position = self.case_face # L'aspirateur se déplace sur la case vide 
            self.case_face = addition(self.case_face,a) # On actualise la case en face
            M[self.position[0],self.position[1]] = 4 # On actualise la position de l'aspirateur
            #print(M)            
        
        elif Case_dans_Matrice (self.case_face,M) == 1 : # Si on est face a un objet
            # cartographier la pièce : 
            self.cartographier(self.case_face)
            if self.case_face[0] != 0 and  self.case_face[0] != self.long +1 and self.case_face[1] != self.larg +1 and self.case_face[1] != 0:
                self.obstacles = ajout_sans_doublon ((self.case_face[0],self.case_face[1]),self.obstacles) # Actualiser la liste des objets si ce n'est pas un mur
                
            # Permet l'évolution de l'aspirateur : 
            self.nb_rotation += 1 # On est face a un objet donc on tourne
            a= Nouvelle_case_face (self.position, self.case_face,p)
            self.case_face = addition(self.case_face,a) # On actualise la case de face
            self.deplacement_aleatoire_ameliore(p) # On relance la fonction 
       
        else : # L'aspirateur est déja passé sur la case en face de nous
            # On regarde les cases autours, y a-t-il des cases encore sales ? :
            for i in range(4): 
                self.nb_rotation += 1
                a= Nouvelle_case_face (self.position, self.case_face,p)
                self.case_face = addition(self.case_face,a)
                # Cartographier : 
                if Case_dans_Matrice (self.case_face,M) == 1 and self.case_face[0] != 0 and  self.case_face[0] != self.long +1 and self.case_face[1] != self.larg +1 and self.case_face[1] != 0:
                    self.obstacles = ajout_sans_doublon ((self.case_face[0],self.case_face[1]),self.obstacles) # Actualise la liste des objets
                # Retour au déplacement
                if Case_dans_Matrice (self.case_face,M) == 0 : # On trouve une case vide autour de l'aspirateur, on avance de ce coté
                    return self.deplacement_aleatoire_ameliore(p)
            # Si on arrive a ce stage, l'aspirateur est entouré de case déja nettoyées ou d'obstacles, on cherche donc à revenir sur nos pas et donc repasser sur une case déja nettoyée
            while Case_dans_Matrice (self.case_face,M) !=3 : # On ne peut que se déplacer sur une case déja nettoyée
                a= Nouvelle_case_face (self.position, self.case_face,p) # On actualise
                self.case_face = addition(self.case_face,a)
            a=[self.case_face[0]-self.position[0] ,self.case_face[1]-self.position[1]]
            M[self.position[0],self.position[1]] = 3
            self.cases_nettoyées =ajout_sans_doublon ([self.position[0],self.position[1]],self.cases_nettoyées)
            self.position = self.case_face # L'aspirateur se déplace sur la case disponible 
            self.case_face = addition(self.case_face,a)
            M[self.position[0],self.position[1]] = 4
            self.nb_deplacements += 1
            self.fin() # On repasse sur une case déja nettoyée, c'est peut être que la pièce est entièrement nettoyée, on vérifie le test de fin.
        #print(M)
        
        
        
 def test_aleatoire(self,e=0.7,Iter=x_longueur*x_largeur*100):

        Cette fonction retourne le nombre de déplacements et de rotations 
        necessaires pour nettoyer entièrement la pièce avec la fonction de
        déplacement déplacement_aleatoire.
        On fixe le paramétre p = 1 par défaut car c'est la valeur de p qui
        minimise le nombre de déplacements et de rotations à effectuer 
        (cf le fichier Tests.py)
        
        Exemple: 
            >>> Robot = Aspirateur()
            >>> Robot.test_aleatoire()
                [91, 130]
                Il faut donct 76 déplacements et 235 rotations pour nettoyer 
                cette pièce.

        i=0

        while self.termine != True and i<Iter:
            self.deplacement_aleatoire(e)
            #print(M)
            i+=1
        if i>=Iter:
            print("Le nombre d'itération est maximal")
        if depart in self.obstacles: 
            self.obstacles.remove(depart)
        return[self.nb_deplacements, self.nb_rotation]
    
'''

#robot=Aspirateur()
#robot.test_aleatoire_ameliore()