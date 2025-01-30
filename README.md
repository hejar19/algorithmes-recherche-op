# 🎯 Algorithmes de Recherche Opérationnelle

## 📌 Description
Ce projet est une application développée en **Python** avec **Tkinter**, permettant d’exécuter et de visualiser plusieurs algorithmes de recherche opérationnelle.  
L’interface graphique est moderne et minimaliste, inspirée du thème Metronic UI.

## 🚀 Installation et Exécution

### 1️⃣ **Cloner le projet**
Ouvrez un terminal et exécutez la commande suivante :
```bash
git clone https://github.com/hejar19/algorithmes-recherche-op.git
cd algorithmes-recherche-op
```

### 2️⃣ **Installer les dépendances**
Assurez-vous d’avoir Python installé, puis exécutez :
```bash
pip install -r requirements.txt
```

### 3️⃣ **Lancer l’application**
Une fois les dépendances installées, lancez l’application avec :
```bash
python main.py
```

---

## 🛠 **Algorithmes Implémentés**
L’application inclut plusieurs algorithmes classiques de recherche opérationnelle :

- ✅ **Welch-Powell** (Coloration des graphes)  
- ✅ **Kruskal** (Arbre couvrant minimal)  
- ✅ **Dijkstra** (Chemin le plus court)  
- ✅ **Ford-Fulkerson** (Flot maximal)  
- ✅ **Bellman-Ford** (Chemin le plus court avec poids négatifs)  
- ✅ **Méthode du coin Nord-Ouest** (Optimisation du transport)  
- ✅ **Méthode du moindre coût** (Optimisation du transport)  
- ✅ **Méthode Stepping Stone** (Optimisation du transport)  
- ✅ **Algorithme de Metra** (Chemin critique en gestion de projet)  

Chaque algorithme est accessible via une interface interactive permettant de **générer des graphes aléatoires**, **visualiser les calculs**, et **afficher les résultats graphiquement**.

---

## 📂 **Structure du projet**
```
algorithmes-recherche-op/
│── logoEmsi.png                 # Image utilisée dans l’interface
│── welcome.py                   # Page d'accueil de l'application
│── interfaceAccueil.py          # Interface principale avec les boutons des algorithmes
│── interfaceWelshPowel.py       # Implémentation de Welch-Powell
│── interfaceKruskal.py          # Implémentation de Kruskal
│── interfaceDijkstra.py         # Implémentation de Dijkstra
│── interfaceBellmanFord.py      # Implémentation de Bellman-Ford
│── interfaceFordFulkerson.py    # Implémentation de Ford-Fulkerson
│── interfaceSteppingStone.py    # Implémentation des méthodes de transport
│── interfacePotentielMetra.py   # Implémentation de l’algorithme de Metra
│── main.py                      # Fichier principal lançant l’application
│── requirements.txt             # Liste des dépendances Python
│── README.md                    # Documentation du projet
```

---

## 📦 **Créer un exécutable**
Si vous souhaitez **générer un fichier exécutable (.exe)**, utilisez **PyInstaller** :

```bash
pyinstaller --onefile --windowed main.py
```
L’exécutable sera généré dans le dossier `dist/`.
