# Plan des slides (9 slides, ~10 min)

Les chiffres viennent du notebook `main.ipynb` : reprendre les graphiques directement
(clic droit sur une figure > copier l'image), et faire une demo du dashboard a la fin.

## 1. Titre
Impact de l'IA generative sur les resultats et le bien-etre des etudiants.
Groupe (5 noms), L3 ESGI, cours Ecosysteme Hadoop.

## 2. Le dataset et la question
Kaggle, 50 000 etudiants, 16 colonnes (GPA avant/apres, heures d'IA, usage, anxiete,
burnout...). Question : l'IA aide-t-elle ou dessert-elle les etudiants ?

## 3. Architecture technique
Schema : CSV -> HDFS (bronze) -> Spark (silver : nettoyage) -> gold (features) -> MLlib / dashboard.
Stack : Hadoop 3.3.6, Spark 4.1.1, PySpark, Python 3.11, Streamlit. Architecture medaillon.

## 4. Nettoyage (silver)
Verifications faites : doublons (0), valeurs manquantes (0), coherence des domaines
(GPA dans [0,4], echelles 1-5 / 1-10, heures) -> dataset tres propre, 0 ligne supprimee.
Montrer 1-2 graphiques (distributions, boxplots).

## 5. Resultat 1 : qui progresse ?
Progression moyenne : +0.20 point de GPA sur le semestre.
Graphique des correlations avec GPA_Delta : le travail classique domine (+0.38),
le volume d'heures d'IA ne joue presque pas (-0.05).

## 6. Resultat 2 : c'est l'usage qui compte, pas la quantite
Barres GPA_Delta par usage : Debugging +0.25 > Ideation/Copywriting/Resume ~+0.20
> Reponses directes +0.13. Usage modere (5-10h) meilleur que intensif (20-40h).
Message : l'IA comme assistant = benefique, l'IA a la place de l'etudiant = penalisant.

## 7. Resultat 3 : trois profils d'etudiants (k-means)
Tableau des 3 clusters : les studieux (41%, +0.32 de GPA, meilleure retention),
les dependants de l'IA (19%, 21h d'IA/sem, anxiete et dependance max),
les peu investis (40%, +0.10). Mentionner le choix de k (silhouette).

## 8. Demo du dashboard Streamlit
Filtres filiere/annee, chiffres cles, progression par groupe (menu deroulant),
profils k-means (tableau + nuage de points).

## 9. Conclusion
L'IA n'est ni bonne ni mauvaise en soi : tout depend de l'usage (assistant vs substitut)
et de l'intensite (usage lourd = dependance et anxiete accrues, cf. profil "dependants de l'IA").
Limites : donnees declaratives, correlation != causalite.
