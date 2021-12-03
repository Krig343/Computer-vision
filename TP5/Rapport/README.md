# Rapport du TP5

Tous ces tests ont été effectué sur l'image *facade.png*

## Détecteur de coins de Harris

### Version 1

#### Robustesse à la transformation

En effectuant une rotation complète de l'image, les points détectés ne changent pas et leurs nombre ne varie pas non plus. Le détecteur de coins de Harris est très robuste à la mise à l'échelle. En effet, aucun changement significatif n'est remarqué en agrandissant l'image à 150% (100 sur la trackbar). En revanche, en se rapprochant d'une taille de 50% de la taille originelle, on note une légère perte de précision aux alentours de 20 sur la trackbar.

#### Robustesse au bruit

La résistance au bruit du détecteur de coins de Harris est assez limité. On remarque très vite une croissance exponentielle du nombre de points (à un écart d'environ 12 dans la fonction random.normal).

#### Robustesse à la tranformation perspective

La déformation perspective n'altère aucunement la détection de coins.
Ce constat à été fait avec les points suivants :
p1 = (125,100)
p2 = (375,100)
p3 = (150,400)
p4 = (350,400)

### Version2

Ma propre implémentation de la détection de coins de Harris présente les forces et faiblesses que la versions d'opencv. À la différence près que cette version est nettement moins efficace de manière générale.

## Détecteur de coins Shi-Tomasi

### Robustesse à la transformation

Le détecteur de Shi-Tomasi est de manière générale moins résistant à la rotation, comme à la mise à l'échelle, que le détecteur de Harris. Cela se voit par une apparation et une disparission de certains même points en fonction de l'angle et du niveau de zoom de l'image. Et ceux peu importe les valeurs prisent pour effectuer les transformations. Cependant, aucune point abérent n'a pu être constaté.

### Robustesse au bruit

Ce détecteur est très robuste vis-à-vis du bruit. Il a fallu monter à un valeure d'écart de 60 avant de ramarquer le premier point affiché sur une surface où aucun point ne se trouve.

### Robustesse à la transformation perspective

En choisissant les points (0,0), (375,0), (125,500) et (500,500), aucun changement au niveau des points affiché n'a été noté. Ce détecteur est donc très résistant face à la transformation perspective.

## Détecteur de points d'intérêts SIFT

Le détecteur n'étant plus présent gratuitement dans les dernières version d'opencv, j'ai du installer une librairie maintenue par la communauté pour pouvoir l'utiliser. Cela vient donc peut-être du mauvaise configuration lors de l'installation, mais lors de mes tests le détecteur SIFT n'était robuste à aucune transformation et était significativement plus mauvais que tous les autres détecteurs.

## Détecteur ORB

### Robustesse à la transformation

Les détecteur ORB est le plus robuste de tous ceux testé dans ce TP. Très peu de variation dans les points n'a été remarquée lors de la rotation. De même pour le rétrécissement de l'image. En revanche, les points affichés ont commencé à devenir incohérent lors d'un grossissement de 20% (70 sur le trackbar).

### Robustesse au bruit

Aucun changement n'a été détecté en ajoutant du bruit.

### Robustesse à la transformation perspective

Aucun changement n'a été détecté lors de la transformation.
Les points utilisés sont (0,0), (375,0), (125,500) et (500,500).

## Détecteur SURF

Le détecteur SURF n'a pas pu être mit en place car il n'est plus supporté de manière gratuite dans cette version de python.