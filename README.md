# Solveur de Motus

## Les règles
Solveur du jeux de Motus disponible [ici](https://wordlegame.org/fr?) ou bien [ici](https://sutom.nocle.fr/).  
  
Le but est de trouver un mot caché.  
Le joueur choisi un mot et le jeu affiche des indices.  
Une lettre marquée en vert est bien placée.  
Une lettre marquée en jaune est mal placée mais appartienX au mot caché.  
Une lettre sans marquage n'appartiens pas au mot caché.  

## Le lexique
lexique_archive.zip  
 - Lexique383.tsv : issu de <http://www.lexique.org>  
 - lexique.txt : liste de mots  
Executez le python extract_lexique.py pour génerer "lexique.txt"

## Le solveur
Le but du solveur est d'aider à trouver le mot caché en le minimum de coups possible
en s'aidant des indices.  

Executez SolveurMotus.py  
5 mots aléatoires sont proposés selon la taille  
Appuyer sur Entrée pour valider un mot  
Cliquez sur une lettre pour changer sa couleur en fonction de ce que le jeux de Motus
propose en parallèle  
Cliquez sur "Vérifier" pour avoir les suggestions  
Cliquez sur une suggestion pour l'entrer dans les cellules directement  
Cliquez sur "Reset" pour réinitialliser la grille  
