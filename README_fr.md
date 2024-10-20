# Attribution des Régions aux Représentants Commerciaux chez Pfizer Turquie

## Description du Travail

Le projet consiste en les tâches suivantes :

- **Décrire la situation et le problème de décision** (parties prenantes, enjeux, données, etc.).
- **Spécifier l'ensemble des choix** et les critères d'évaluation.
- **Calculer des solutions efficaces**.
- **Discriminer les solutions à l'aide d'un modèle additif**.
- **Analyser les limites** du modèle proposé.

## Questions Clés

Abordez les questions suivantes :

1. **Propriétés des solutions** : Les solutions obtenues présentent-elles des propriétés qui méritent d'être portées à l'attention du décideur ?
2. **Comparaison des solutions** : Comparez les propriétés de la solution actuelle avec celles que vous avez obtenues.
3. **Variation de la charge de travail** : La charge de travail est actuellement modélisée comme une contrainte. Essayez de modifier cette contrainte (par exemple, en utilisant l'intervalle [0,9, 1,1]), et discutez de son impact sur l'ensemble des solutions et les compromis avec d'autres objectifs.
4. **Assignation partielle des zones** : Comment le modèle peut-il gérer l'assignation partielle des zones (c'est-à-dire l'assignation d'une zone à plusieurs représentants commerciaux) ? Implémentez cela et comparez les résultats.
5. **Augmentation de la demande** : Si la demande augmente de manière uniforme (par exemple, +20 %), il pourrait être nécessaire de recruter un nouveau représentant commercial. Discutez de l'endroit où localiser son bureau (zone centrale).
6. **Localisation des zones centrales** : La localisation des bureaux des représentants commerciaux (zones centrales) influence les distances parcourues. Comment le modèle peut-il être généralisé pour permettre une modification des zones centrales ? Cela nécessite l'ajout de variables binaires supplémentaires. Notez que certaines zones peuvent ne pas être de bons candidats en tant que "zone centrale", ce qui permet de réduire le nombre de variables.
7. **Préférences des représentants commerciaux** : Comment le modèle peut-il intégrer les préférences des représentants commerciaux pour leur région assignée ?

## Outils

Choisissez un **solveur/modéliseur** approprié pour implémenter la solution.
