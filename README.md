# JEU DU TAQUIN

## Description du jeu
Le but est de reconstituer un puzzle en déplaçant les pièces une à une jusqu'à ce que le puzzle soit reconstitué. 
Ceci est l'image avant le shuffle, ainsi que celle à reconstituer:
<code>
        [1 2 3]
        [4 5 6]
        [7 8 0]
</code>

Une fois mélangé, le puzzle peut ressembler à ceci:
<code>
        [7 4 1]
        [2 0 8]
        [3 5 6]
</code>
<br>
Nous avons créé une IA qui suit l'algorithme A* pour résoudre le puzzle, selon deux heuristiques:<br>
<p style="text-decoration : underline">-Heuristique de Hamming :</p> 
    <code>Le nombre de pièces mal placées</code>
<br>
<p style="text-decoration : underline">-Heuristique de Manhattan :</p> 
    <code>La somme des distances de Manhattan entre les pièces et leur position cible</code>
<br><br><br>
Étant donné que l'heuristique de Manhattan va chercher directement le chemin le plus court, elle est plus efficace que l'heuristique de Hamming, qui elle, exécutera une recherche bien plus profonde.

## Récupération du projet
Dans votre terminal, rendez-vous au répertoire souhaité, et tapez la commande suivante:<br>
```git clone https://github.com/maximeabade/Taquin_A_Star.git```

## Comment jouer
Vérifiez votre installation de Python3 avec la commande suivante:<br>
```python3 --version```<br>
Rendez-vous dans le répertoire et lancez la résolution avec la commande suivante:<br>
```python3 Taquin_main.py```

## Résultats
On trouve le même nombre d'étapes pour résoudre le problème, mais on remarque de suite qu'effectivement, l'heuristique de Manhattan est plus efficace que l'heuristique de Hamming, car elle exécute moins de noeuds, et donc moins de calculs.