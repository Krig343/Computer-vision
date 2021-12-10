# Travaux pratiques : séance 6

L'objectif de ce TP est de créer une image panoramique construite à partir de deux images ou plus acquises en rotation sur un pied. 
On rappelle qu'il existe une transformation homographique $`H`$ entre ces images.


## Exercice 1 : appariement des points d'intérêt de Harris

Dans un premier temps, on souhaite s'appuyer sur le détecteur de coins de Harris pour apparier les points similaires entre deux images.
Pour ce faire, on va associer à chaque point de Harris un descripteur de son voisinage local. Plus précisément, le descripteur associé à un point d'intérêt sera formé par un vecteur contenant les valeurs des pixels dans un voisinage $`n*n`$ autour de ce point.

L'appariement des points selon leur descripteur se fera au plus proche voisin, en utilisant la norme $`L_2`$.

## Appariement 

Écrire un programme qui prend deux images A et B en entrée, calcule les points d'intérêt de Harris en fonction d'un certain nombre de paramètres passés en ligne de commande puis affiche une image composée des deux images A et B côte à côte, et où chaque appariement entre couple de points est modélisé par une ligne entre ces deux points.

## Calcul d'homographie

Le programme calcule maintenant l'homographie $`H`$ entre les images à partir des points appariés, et affiche les deux images A et H(B) côte à côte.
Vous pourrez vous appuyer sur l'algorithme RANSAC qui permet de calculer une homographie entre deux ensemble de points contenant potentiellement des outliers :

Faire :
1. Tirage aléatoire de quatre couples de points appariés (ensemble A vers ensemble B)
2. Calcul d'une homographie H' à partir de ces points
3. Transformation des points de l'ensemble B par l'homographie H'
4. Calcul de la distance moyenne entre les points A et H'(B)
   
Tant que cette distance est supérieure à un seuil $`\epsilon`$


## Assemblage des images

Le programme final assemble maintenant les deux images obtenues et affiche le résultat

## Exercice 2 : assemblage d'image à partir de SIFT et ORB

Les descripteurs calculés précédemment ont un problème important : ils sont peu robustes, et en particuliers pas invariants à la rotation et au changement d'échelle.
Les descripteurs codés dans SIFT sont plus robustes, car ils sont invariants à un certain nombre de transformations. 

En vous appuyant sur toutes les fonctions de la librairie OpenCV et la documentation https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html et https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html , écrire un programme permettant d'assembler deux images ou plus en vous appuyant sur les descripteurs SIFT puis ORB.



