# Impact de l'IA generative sur les etudiants - Hadoop / PySpark

Projet de groupe L3 ESGI. Analyse du dataset Kaggle `ai_student_impact_dataset.csv`
(50 000 etudiants, 16 colonnes) avec une architecture medaillon (bronze / silver / gold)
sur HDFS, PySpark pour le traitement et Spark MLlib pour le machine learning.

## Contenu

- `main.ipynb` - tout le pipeline :
  - **Bronze** : chargement du CSV brut dans HDFS
  - **Silver** : nettoyage (doublons, valeurs manquantes, coherence), stats descriptives, visualisations
  - **Gold** : features (GPA_Delta, encodages ordinaux)
  - **Analyse** : quels criteres font varier la note (correlations, moyennes par groupe)
  - **ML** : clustering k-means -> 3 profils d'etudiants
  - Export de `gold_dashboard.csv` pour le dashboard
- `app.py` - dashboard Streamlit (filtres, chiffres cles, progression par groupe, profils k-means)

## Installation

```
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env    (puis renseigner JAVA_HOME = chemin du JDK 17)
```

## Lancer le projet

```
# 1. Demarrer Hadoop (fenetre cmd separee)
start-dfs.cmd
start-yarn.cmd

# 2. Executer main.ipynb dans VSCode (kernel : .venv 3.11.9)
#    -> genere gold_dashboard.csv

# 3. Lancer le dashboard
streamlit run app.py
```

## Interfaces web

- http://localhost:9870 -> NameNode (HDFS)
- http://localhost:9864 -> DataNode
- http://localhost:8088 -> ResourceManager (YARN)

## Resultats principaux

- Les etudiants progressent en moyenne de **+0.20 point de GPA** sur le semestre.
- Le 1er facteur de progression reste le **travail personnel classique** (corr. +0.38),
  loin devant le volume d'heures d'IA (quasi nul : -0.05).
- C'est **le type d'usage de l'IA qui compte** : debugging +0.25 vs generation directe
  de reponses +0.13 (seul usage nettement penalisant).
- **3 profils d'etudiants** (k-means) : les studieux (41%), les dependants de l'IA (19%),
  les peu investis (40%).