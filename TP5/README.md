# Travaux pratiques : séance 5

Dans ce TP on va s'intéresser à la détection de points d'« intérêt » dans une image.
Il n'existe pas de définition précise de ce qu'est un point d'intérêt : idéalement, un point d'intérêt doit être associé à une structure ou région saillante ou perceptuellement significative de l'image.
L'objectif recherché est que, étant donné une image et une certaine définition de points d'intérêts, on puisse retrouver les mêmes points dans l'image déformée par un ensemble de transformations géométriques, photométriques (variation d'illumination) ou altérations diverses (bruit, occlusions, etc.).

Les méthodes de détection de points d'intérêt qui sont développées poursuivent deux principaux objectifs :

* assurer une certaine stabilité  ou invariance des points détectés à des transformations géométriques plus ou moins complexes : translation, rotation, mise à l'échelle, transformations projectives...
* obtenir un nombre de points suffisants, mais pas trop élevé


## Travail évalué 

Rapport à rendre sous forme de fichier `README.md` dans votre dépôt git.
Ce rapport doit contenir, pour chaque descripteur étudié, un ensemble de jeux d'essais permettant d'évaluer qualitativement la robustesse du descripteur aux différentes transformations étudiées.

# Exercice 1 : détecteur de coins de Harris (Harris corner detector)

L'objectif de cette méthode est de détecter les « coins » de l'image. L'hypothèse est que les « coins » d'une image sont suffisamment caractéristiques pour être présents dans les différentes transformations d'une image.

Le principe de la méthode est expliqué ici : 
https://docs.opencv.org/4.x/dc/d0d/tutorial_py_features_harris.html

Vous pourrez également consulter https://docs.opencv.org/4.x/df/d54/tutorial_py_features_meaning.html pour une introduction sur les points d'intérêt.

## Version 1 : implémentation OpenCV

Écrire un programme qui calcule les coins de Harris sur une image passée en paramètres, en vous appuyant sur la fonction `cornerHarris` de la bibliothèque OpenCV. 
En utilisant cette fonction, on souhaite conserver les points qui :

* ont une valeur supérieure à un certain seuil (0.01* la valeur maximale, comme dans l'exemple proposé dans la documentation)
* sont des maxima locaux dans un voisinage 3x3

On affichera en rouge les points détectés.
On pourra [dilater](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html) les points obtenus afin de les rendre plus visibles.

## Stabilité à la rotation et à la mise à l'échelle

On veut maintenant évaluer l'invariance de cet opérateur à la rotation et la mise à l'échelle.

Reprendre le programme précédent et ajouter deux trackbars : une trackbar pour faire varier l'angle de rotation, et une pour faire varier le coefficient de mise à l'échelle (entre 50% et 150%).
Afficher les points de Harris calculés pour chaque mise à jour des transformations.
Comparer visuellement les points obtenus entre les différentes transformations, pour plusieurs images. 

## Version 2 : implémentation propre

On va reprendre le programme précédent, mais en implémentant la méthode de détection de coins de Harris (sans s'appuyer sur la méthode d'OpenCV donc).

Le principe de la méthode est le suivant : on cherche les points de l'image dans le voisinage desquels la variation est forte dans deux directions orthogonales. Pour cela, on s'appuie d'une part sur le calcul des variations horizontales et verticales (c'est à dire le gradient de l'image), d'autre part sur la matrice $`M`$ de covariance du gradient.

Soient $`I_x`$ et $`I_y`$ les images du gradient horizontal et vertical, respectivement.
La matrice  $`M`$  est définie en fonction d'un point $`x`$ par :

$` 
M(x)=\sum_{x\in \mathbf w}
\begin{bmatrix}
I_x^2(x) & I_{xy}(x) \\
I_{xy}(x) & I_y^2(x) \\
\end{bmatrix}
`$

où $`I_{xy}(x)=I_x(x)*I_y(x)`$ et $`\mathbf w`$ est un petit voisinage autour du point (par exemple 3x3 ou 5x5). La taille de ce voisinage correspond au paramètre `blockSize`de la fonction `cornerHarris(...)`.

1. Calculer $`I_x`$ et $`I_y`$ (en s'appuyant sur les filtres de Sobel par exemple)
2. Calculer les trois images $`\sum_{x\in \mathbf w} I_x^2`$, $`\sum_{x\in \mathbf w} I_y^2`$, $`\sum_{x\in \mathbf w} I_{xy}`$
3. Calculer l'image (`float32`) $`R`$ définie en chaque point $`x`$ par la valeur : $`R(x)=det(M(x))-k*trace(M(x))^2)`$. Cette image correspond à l'image retournée par la fonction $`cornerHarris(...)`$ et le paramètre $`k`$ correspond au même paramètre de cette fonction.

4. Seuillage et suppression des points non-maximaux :  comme précédemment, ne conserver que les points dont la valeur est supérieure à un certain seuil et qui sont des maxima locaux dans un petit voisinage.

Tester votre implémentation, évaluer qualitativement la robustesse aux transformations (rotation, mise à l'échelle) et la comparer avec celle d'OpenCV.

## Robustesse au bruit

On veut tester la robustesse au bruit des coins de Harris. Dans ce but, écrire une fonction qui ajoute à une image du bruit gaussien d'écart-type $`\sigma`$ passé en paramètre (fonction `np.random.normal(...)`). 
En ajoutant une trackbar qui permet de faire varier interactivement la quantité de bruit, évaluer qualitativement la stabilité des points détectés.


## Robustesse à la transformation projective

On veut tester la robustesse des coins de Harris à la transformation projective.
Transformer le programme précédent de manière à pouvoir appliquer de manière interactive une transformation projective sur l'image en spécifiant 4 points de contrôle.

# Exercice 2 : Shi-Tomasi Corner Detector

Le détecteur de coins de Shi-Tomasi modifie le critère de Harris (le score R) de manière à calculer le minimum des des valeurs propres de la matrice de covariance du gradient. Voir :

https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html

## Robustesse à la rotation et la mise à l'échelle

Reprendre le programme de l'exercice 1, mais remplacer le détecteur de Harris par le détecteur de Shi-Tomasi en vous appuyant sur la fonction OpenCV correspondante.
Évaluer qualitativement la robustesse aux transformations géométriques.

## Robustesse au bruit 

Évaluer la robustesse au bruit de ce détecteur.

## Robustesse à la transformation projective

On veut tester la robustesse des coins de Shi-Tomasi à la transformation projective.
Transformer le programme précédent de manière à pouvoir appliquer de manière interactive une transformation projective sur l'image en spécifiant 4 points de contrôle.

# Exercice 3 : SIFT  (Scale Invariant Features Transform)

Le détecteur de points d'intérêt appelé SIFT est très populaire. Il a été introduit par Lowe en 2004 dans cet article :
https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf

Le principe est résumé ici :
https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html

L'intérêt de ce détecteur est qu'il fournit des points qui sont relativement stables par rapport à différentes transformations, dont le changement d'échelle.

D'autre part, les points d'intérêt détectés peuvent être enrichis par un vecteur d'attribut qui caractérise le voisinage spatial autour de chaque point. Dans ce cas, on parle de *descripteur SIFT*.

## Robustesse à la rotation et la mise à l'échelle

Reprendre le programme de l'exercice 1, mais remplacer le détecteur de Harris par le détecteur SIFT en vous appuyant sur la fonction OpenCV correspondante. On affichera les points détectés de la même manière que dans les exercices précédents (sans utiliser la fonction `cv2.drawKeypoints(...)`). Vous pourrez utiliser la fonction `cv2.KeyPoint_convert(...)` pour convertir les structures `KeyPoint` en liste de points.
Évaluer qualitativement la robustesse aux transformations géométriques.

## Robustesse au bruit 

Évaluer la robustesse au bruit de ce détecteur.


## Robustesse à la transformation projective

On veut tester la robustesse des points caractéristiques SIFT à la transformation projective.
Transformer le programme précédent de manière à pouvoir appliquer de manière interactive une transformation projective sur l'image en spécifiant 4 points de contrôle.


# Exercice 4 : autres descripteurs

Le descripteur SIFT est coûteux à calculer, ce qui peut poser des problèmes pour une utilisation en temps-réel.
Des alternatives existent : SURF, ORB,... 
Expérimenter ces descripteurs en les intégrant dans les programmes précédentes et évaluer leur robustesse aux transformations géométriques et au bruit.



