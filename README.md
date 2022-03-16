# Projet d'Algorithmique
## Transformée de Burrows-Wheeler et Codage de Huffman

Ce projet a été réalisé dans le cadre de l'UE Algorithmique pour la bioinformatique du Masteer Bioinformatique DLAD  
Projet développé sous Python Python 3.10.0
<hr>

# Instruction
- Installer l'ensemble des librairies listées dans le [requirement.txt](requirements.txt).  
```bash
  pip install -r requirement.txt
```
- Lancer le programme avec la ligne suivant :

```bash
  python3 interface.py
```
- Entrer dans une séquence dans le champ d'entrée ou bien utiliser le bouton parcourir pour choisir un fichier local
- Choisir une des fonctions via les boutons (seulement les fonctions prennant en entrée une séquence)
- Les resultats apparaissent dans une nouvelle fênetre où un bouton "Sauvegarder" permet d'enregistrer les resultats dans un fichier texte

- Pour les fonctions Huffman n'utilisant pas une séquence en entré, il faut mettre les fichiers créer par les fonctions précèdent  
Exemple: Pour utiliser le bouton Binaire vers ASCII il faut utiliser en donnée d'entrée le resultats du bouton Sequence vers binaire.
<hr>

## Presentation des boutons

- Sequence vers BWT: Affiche le transformée de Burrows-Wheeler  

- Sequence vers BWT étape par étape: Affiche la liste de séquence permettant d'obtenir le transformée de Burrows-Wheeler  
- BWT vers sequence: Affiche la séquence initiale à partir du transformée de Burrows-Wheeler  
- BWT vers sequence: Affiche chaque étape de la construction de la matrix permettant de retrouver la séquence initiale  
- Sequence vers Huffman: Depuis une séquence ou bien un transformée de BWT compressé celle-ci directement en charactère ASCII
- Huffman vers sequence: Depuis un fichier compressé, permet de le décompressé pour obtenir l'entrée initiale
- Sequence vers binaire: Affiche la traduction d'un fichier d'entrée en binaire
- Binaire vers sequence: Affiche la traduction d'une séquence binaire en séquence
- Binaire vers ASCII: Affiche la traduction d'un fichier binaire en charactère ASCII
- ASCII vers binaire: Affiche la traduction d'un fichier ASCII en binaire


