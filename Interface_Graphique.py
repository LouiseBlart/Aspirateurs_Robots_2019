# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:40:19 2020

@author: Yvan Belakebi-Joly et Louise Blart
"""

"""
Ce fichier crée une interface graphique permettant à l'utilisateur d'entrer 
les dimensions de la pièce et d'insérer manuellement les objets où il le souhaite. 
Ces éléments nous seront utiles pour permettre le déplacement complet de 
l'aspirateur.

Ce fichier n'est pas à executer seul, il sera utilié dans le fichier Deplacement.
"""

from tkinter import * 
from tkinter.messagebox import *
from Commandes import * 
from PIL import *


# Récupérer les dimensions de la piece :
def recupere():
    '''
    Fonction qui permet de récupérer les dimensions (largeur et longueur de la
    pièce, taille des cases) insérées par l'utilisateur 
    
    '''
    if (OnValidate(entree_largeur.get()),OnValidate(entree_longueur.get()), OnValidate(entree_case.get())) == (True,True,True): # Si les valeurs entrées par l'utilisateur son bien dans les normes
        global x_largeur, x_longueur, x_case # On récupére les variables pour en faire des variables globales
        x_largeur = int(entree_largeur.get()) # On les converti en entier 
        x_longueur=int(entree_longueur.get())
        x_case = int(entree_case.get())
        showinfo("info", "Merci ! ") 
        window_info.destroy()
    else: # Les valeurs entrées ne sont pas utilisables
        showerror("Alerte","Les valeurs largeur, longueur et taille des cases doivent être des entiers strictement supérieurs à 0")

def rectangle(x, y, coul):
    """
    trace un rectangle de dimension x, y et de couleur 'coul'
    Cela nous permettra de représenter les obstacles de la pièce.
    """
    can.create_rectangle(x-x_case/2, y-x_case/2, x+x_case/2, y+x_case/2, fill=coul)  
    
liste_objet=[] # Nous permet de vérifier la concordance entre les objets placés et les coordonnées trouvées
def objet (event):
    """Dessine un objet là où l'utilisateur a cliqué"""
    x=event.x%x_case # On récupére les coordonnées là où l'utilisateur a cliqué
    x=int((event.x-x)+x_case/2) # x_case/2 afin de récupérer le centre du carré où il clique
    y=event.y%x_case
    y=int((event.y-y)+x_case/2)
    global liste_objet # permet d'implémenter la variable globale liste_objet
    liste_objet.append([y,x])
    rectangle(x,y,"brown") # Crée un rectangle de couleur marron a l'endroit choisi pour poser un objet.
    
    
depart_aspirateur =[] # Nous servira pour le déplacement de l'aspirateur
def aspirateur (event):
    """ 
    Cette fonction permet à l'utilisateur d'insérer l'aspirateur par l'intermédiaire
    du clic droit de sa souris (il ne peut pas poser l'aspirateur sur un obstacle)
    """
    x=event.x%x_case #On récupére les coordonnées du clic de de l'utilisateur
    x=int((event.x-x)+x_case/2)
    y=event.y%x_case
    y=int((event.y-y)+x_case/2)

    if IsIn (liste_objet,[y,x]) == True : # Impossible de poser l'aspirateur sur un obstacle
        showinfo("Erreur", "L'aspirateur ne peut pas être sur un objet ! ")
        can.bind("<Button-3>",aspirateur) 
    else : # l'aspirateur est placé sur une clase libre
        global depart_aspirateur
        depart_aspirateur.append([y,x]) # On implémente la variable départ_aspirateur
        rectangle (x,y,coul='red') 
        can.create_image(x,y,image=image) # L'aspirateur est représenté sur notre canvas par une petite photo d'aspirateur
        label_aspirateur.pack_forget() # On retire l'information indiquant à l'utilisateur de placer l'aspirateur
    if len(depart_aspirateur)>=1 :
        can.unbind("<Button-3>", can.bind("<Button-3>", aspirateur)) # On empéche l'utilisateur de placer plusieurs aspirateurs
        showinfo("info", "Merci ! ") 
        window_grille.destroy() # Une fois l'aspirateur placé nous pouvons quitter l'interface graphique, le reste du projet se fera dans la console de Spyder
        
def desactiver_liaison ():
    '''
    Cette fonction permet de désactivé la liaison entre le clic gauche et la 
    pose d'obstacle dès que l'utilisateur a validé sa pièce.
    '''
    can.unbind("<Button-1>", can.bind("<Button-1>", objet))
    label_objet.pack_forget()
    bouton_valider_objet.pack_forget()
    placer_aspirateur()

    
def placer_aspirateur ():
    '''
    Cette fonction lie le clic droit de la souris à la pose de l'aspirateur dans
    la pièce.
    '''
    global label_aspirateur
    label_aspirateur = Label(frame_grille, text="Clic droit pour placer l'aspirateur",bg='#0E3821',fg='white')
    label_aspirateur.pack(side=TOP)
    can.bind("<Button-3>",aspirateur)

# Créer la fenêtre informations  :
window_info=Tk()
window_info.title("Information") # Titre de la fenetre
window_info.iconbitmap("information.ico") # ajouter un logo en haut a gauche de la fenetre
window_info.config(background='#41B77F') # configuration de la couleur d'arrière plan

# Création de la partie information : Cette fenetre permet a l'utilisateur d'entrer les dimensions de la pièce
frame_largeur = Frame(window_info ,bg='#41B77F')
frame_longueur = Frame(window_info ,bg='#41B77F')
frame_case= Frame(window_info ,bg='#41B77F')

## Créer des labels : Permet de guider l'utilisateur
largeur = Label(frame_largeur, text="Insérer la largeur de la piece :",bg='#41B77F')
largeur.pack()
longeur = Label(frame_longueur, text="Insérer la longueur de la piece :",bg='#41B77F')
longeur.pack()
case = Label(frame_case, text="Insérer la taille de chaque carreau de la piece, \n afin d'ajuster la grille à la dimension de votre écran :",bg='#41B77F')
case.pack()

# Créer des champs/input
# Champs de la largeur de la pièce
largeur = IntVar() 
entree_largeur = Entry(frame_largeur, textvariable=int, width=10) # afin de récupérer ce que l'utilisateur a entré.
entree_largeur.pack()
# Champs de la longueur de la pièce
value = IntVar() 
entree_longueur = Entry(frame_longueur, textvariable=int, width=10)
entree_longueur.pack()
# Champs pour la taille de chaque case de la piece 
case = IntVar() 
entree_case = Entry(frame_case, textvariable=int, width=10)
entree_case.pack()

# Récupérer les dimensions de la piece 
bouton = Button(window_info, text="Valider", command=recupere) # On récupére toutes les données entrées par l'utilisateur pour créer la pièce
bouton.pack( side=BOTTOM)

# On referme tout, notre fenetre d'informations est terminée. 
frame_largeur.pack(side=LEFT, padx=30, pady=30)
frame_longueur.pack(side=LEFT, padx=30, pady=30)
frame_case.pack(side=LEFT, padx=30, pady=30)
window_info.mainloop()



window_grille=Tk() # On recrée une nouvelle fenetre pour représenter la pièce, insérer l'aspirateur et les objets
window_grille.title("Mon super Aspirateur") # Nom de la fenétre
window_grille.iconbitmap("cleaning.ico") # ajouter un logo en haut a gauche de la fenetre
window_grille.config(background='#41B77F')
img = Image.open('cleaning.png') # image extension *.png,*.jpg
img = img.resize((x_case, x_case), Image.ANTIALIAS) # Pour redimensionner l'aspirateur à la dimension des cases
img.save('cleaning_dim.png') # On enregistre l'image
image = PhotoImage(file='cleaning_dim.png')

frame_grille = Frame(window_grille, bg='#41B77F') # On crée la frame grille.

can = Canvas(window_grille, width =x_largeur*x_case-4, height =x_longueur*x_case-4, bg ='white') # On représente les dimensions de la pièce

def grille ():
    '''
    Cette fonction permet de dessiner la grille dans notre canvas en fonction 
    des dimensions  insérées par l'utilisateur.
    '''           
    l=0
    L=0
    while L<(x_longueur)*x_case:
        can.create_line(0,L,x_largeur*x_case,L)
        L+=x_case
    while l<(x_largeur)*x_case:
        can.create_line(l,0,l,x_longueur*x_case)
        l+=x_case

grille()

label_objet = Label(frame_grille, text="Clic gauche pour placer les objets",bg='#0E3821',fg='white') # Guide pour l'utilisateur
label_objet.pack(side=TOP)
can.bind("<Button-1>", objet)
bouton_valider_objet = Button(frame_grille, text="Valider",command=desactiver_liaison) # On désactive la liaison entre la création d'obstable et le clic gauche une fois que l'utilisateur a validé sa saisie
bouton_valider_objet.pack(side=BOTTOM)



can.pack()
frame_grille.pack(side=BOTTOM) # On referme tout
window_grille.mainloop() # afficher la fenetre 