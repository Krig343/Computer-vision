# Travaux pratiques : séance 7

Ce TP est évalué et à rendre pour le **13 janvier**. Il fera l'objet d'un rapport au format Markdown (`README.md` dans votre dépôt), qui contiendra un résumé de vos travaux et des illustrations des résultats sous forme de jeux d'essais.
Des démonstrations auront lieu lors de la séance du 13 janvier.

Ce sujet prend la forme d'un mini-projet dont le thème est au choix.

## Sujet 1 : stéréovision

Dans ce sujet on souhaite implémenter un algorithme de calcul de carte de disparité pour une utilisation en stéréovision.
L'objectif est de comparer une implémentation propre avec une implémentation s'appuyant sur OpenCV. Vous pourrez tester vos approches sur des images issues de la base de données https://vision.middlebury.edu/stereo/data/ . Vous pourrez reconstruire la carte 3D et la visualiser avec un logiciel tel que MeshLab https://www.meshlab.net/


## Sujet 2 : redimensionnement liquide

Le redimensionnement liquide ou *seam carving* est une technique de redimensionnement d'image permettant de conserver les éléments perceptuellement importants. 
Un descriptif par les auteurs de cette méthode est disponible ici : https://www.youtube.com/watch?v=6NcIJXTlugc&ab_channel=r3dux
La méthode est décrite ici : https://fr.wikipedia.org/wiki/Seam_carving

L'objectif est d'implémenter l'algorithme de redimensionnement liquide en Python et de le tester sur un ensemble d'images. Une interface graphique permettant de modifier interactivement la taille de l'image ou de marquer l'objet d'intérêt à conserver pourra être envisagée.
Vous pourrez comparer votre approche avec celle implémentée dans `scikit-image` : https://scikit-image.org/docs/0.13.x/auto_examples/transform/plot_seam_carving.html

## Sujet 3 : suivi d'objets en temps-réel

L'objectif est d'implémenter un programme qui permet de suivre un objet en temps-réel à partir d'un flux vidéo.
L'objet à suivre pourra être sélectionné interactivement. Le suivi sera matérialisé par une ellipse inscrite dans l'objet. Vous pourrez vous appuyer sur l'algorithme CamShift : https://fr.wikipedia.org/wiki/Camshift 

## Sujet 4 : soustraction de fond

L'objectif est d'implémenter un programme permettant de remplacer le fond d'un flux vidéo par une image passée en paramètre. Plus précisément, les objets dynamiques (qui se déplacent) seront superposés à l'image de fond.


## Sujet 5 : thématique libre

Tout sujet en lien avec la vision par ordinateur : envoyez une proposition à b.naegel@unistra.fr pour validation.