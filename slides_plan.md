# Plan des slides (9 slides, ~10 min)

Les chiffres viennent du notebook `main.ipynb`. Reprendre les graphiques directement
(clic droit sur une figure > copier l'image) et finir par une demo du dashboard Streamlit.

## 1. Titre
Impact de l'IA generative sur les resultats et le bien-etre des etudiants.
Groupe (noms), L3 ESGI, cours Ecosysteme Hadoop.

## 2. Le dataset et la question
Kaggle, 50 000 etudiants, 16 colonnes (GPA avant/apres, heures d'IA, usage, anxiete,
burnout...). Question : l'IA aide-t-elle ou dessert-elle les etudiants ?

## 3. Architecture technique
Schema : CSV -> HDFS (bronze) -> Spark (silver : nettoyage) -> gold (features) -> MLlib / dashboard.
Stack : Hadoop, Spark 4.1.1, PySpark, Python 3.11, Streamlit. Architecture medaillon (bronze/silver/gold).

## 4. Nettoyage (silver)
Verifications : doublons (0), valeurs manquantes (0), coherence des domaines
(GPA dans [0,4], echelles 1-5 / 1-10, heures) -> dataset tres propre, 0 ligne supprimee.
Montrer 1-2 graphiques (distributions, boxplots).

## 5. Resultat 1 : qui progresse ?
Progression moyenne : +0.20 point de GPA sur le semestre.
Graphique des correlations avec GPA_Delta : le travail personnel classique domine (+0.38),
le volume d'heures d'IA ne joue presque pas (-0.05).

## 6. Resultat 2 : c'est l'usage qui compte, pas la quantite
Barres GPA_Delta par usage : Debugging +0.25 > Ideation/Copywriting/Resume ~+0.20
> Reponses directes +0.13. Usage modere (5-10h) meilleur qu'intensif (20-40h).
Message : l'IA comme assistant = benefique, l'IA a la place de l'etudiant = penalisant.

## 7. Resultat 3 : trois profils d'etudiants (k-means)
Choix de k par score de silhouette, k=3. Les 3 clusters :
- Utilisateurs experts (38%, +0.235 de GPA) : IA moderee (6h), meilleure retention (82),
  plus de diversite d'outils et de maitrise du prompt -> le profil le plus sain.
- Usage modere (45%, +0.193) : peu d'IA (5h), un seul outil, faible niveau de prompt.
- Dependants IA (17%, +0.158) : 22h d'IA/sem, dependance (6.1) et anxiete (5.9) les plus
  elevees, retention la plus faible -> le profil a risque, qui progresse le moins.

## 8. Demo du dashboard Streamlit
`streamlit run app.py`. 5 onglets qui reprennent l'analyse gold de maniere interactive :
vue d'ensemble (chiffres cles + histogramme GPA_Delta), facteurs (correlations + heatmap),
progression par groupe, distributions, profils k-means (effectifs + tableau des moyennes).

## 9. Conclusion
L'IA n'est ni bonne ni mauvaise en soi : tout depend de l'usage (assistant vs substitut)
et de l'intensite (usage lourd = dependance et anxiete accrues, cf. profil "dependants IA").
Limites : donnees declaratives, correlation != causalite.
