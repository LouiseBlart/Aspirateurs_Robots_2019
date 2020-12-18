# Les aspirateurs robots 
Belakebi-Joly Yvan & Blart Louise 
Projet de Programmation 1A-ENSAE (2019-2020) 

Les robots aspirateurs font leur première apparition en 2002. Depuis on les retrouve de plus en plus dans nos appartements et maisons. Nous nous intéressons à la programmation de ces aspirateurs robots. 
Comment nettoyer une pièce le plus efficacement possible ? Nous voulons que notre aspirateur nettoie l’intégralité d’une pièce inconnue (largeur, longueur et disposition des obstacles inconnues) le plus rapidement possible (i.e en effectuant le moins de rotations et de déplacements possibles). L’aspirateur que nous programmons a des capteurs sur le devant, c’est pourquoi il peut seulement avancer d’une case ou effectuer une rotation.

Nous avons commencé par établir une interface graphique permettant au propriétaire de l’aspirateur de définir une pièce et de placer les objets. Nous aurions également pu faire cela de manière aléatoire mais nous trouvions plus cohérent d’interroger l’utilisateur. 
Dans un premier temps, toutes ces données sont inconnues pour le robot.

Le choix de l’interface graphique reflète un goût pour la découverte d’un nouveau module (Tkinter) puisque nous n’avions jamais programmé d’interface graphique. Cependant nous avons rencontré quelques difficultés (notamment la récupération de la couleur d’un pixel dans un canvas) qui nous a contraint à repasser sous forme matricielle pour simplifier l’algorithme. (Nous gardons l’interface graphique pour permettre la création de la pièce d’une façon plus ludique pour l’utilisateur.)

A partir de là nous avons programmé différentes fonctions de déplacements plus ou moins efficaces. Nous les avons optimisées en fonction des paramètres aléatoire comme indiqué dans le fichier « Tests.py ». La principale difficulté que nous avons rencontrée dans l’élaboration de ces fonctions de déplacements a été de définir la condition d’arrêt de l’aspirateur, étant donné qu’il ne connait pas les dimensions de la pièce. Cela rend nos fonctions de déplacements peu fiables puisque dès que la pièce devient grande, ou présente de nombreux objets notre programme de déplacement ne lui permet pas de trouver rapidement les dernières cases non nettoyées.

Dans notre dernière fonction de déplacement nous rajoutons l’hypothèse que l’aspirateur connait les dimensions de la pièce. Cette dernière hypothèse nous permet de faire une liste des cases restant à nettoyer à la fin d'une phase d'exploration utilisant les fonctions aléatoires précédentes. Nous programmons donc une fonction qui ira droit vers ces cases en parcourant la pièce de bas en haut et en reliant deux cases non nettoyées par un chemin trouvé à l'aide de l'algorithme de Dijkstra. La bonne application de cette fonction repose sur l'hypothèse que la majorité des obstacles ont déjà été découverts puisque chaque fois qu'un obstacle inconnu est heurté, le calcul doit recommencer. 
En plus d'éliminer l'aléa, cette méthode présente l'avantage de considérer comme obstacle toute case inaccessible depuis la position de l'aspirateur, des obstacles très volumineux comme un canapé ne poseront donc plus problème pour la terminaison des fonctions. Ces fonctions permettent d'optimiser le chemin parcouru mais elles sont très coûteuses, notamment en terme d'espace mémoire. 

Ceci nous amène à évaluer l'économie de déplacement réalisée pour trancher sur l'intérêt de cette méthode. Cependant nous rencontrons des difficultés pour appliquer cette fonction à de vastes pièces.
Finalement nous comparons nos différentes méthodes de déplacements en comptabilisant le taux de réussite de chaque méthode puis le nombre de déplacement qu’elles demandent avant de nettoyer l’intégralité de la pièce.
