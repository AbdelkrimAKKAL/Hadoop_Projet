# Dashboard Streamlit - impact de l'IA generative sur les etudiants
# Necessite gold_dashboard.csv (genere par main.ipynb), puis : streamlit run app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Impact IA - Etudiants", layout="wide")
st.title("Impact de l'IA generative sur les etudiants")

df = pd.read_csv("gold_dashboard.csv")

NOMS_CLUSTERS = {0: "Les studieux", 1: "Les dependants de l'IA", 2: "Les peu investis"}
df["Profil"] = df["Cluster"].map(NOMS_CLUSTERS)

# Filtres (barre laterale)
st.sidebar.header("Filtres")
filieres = st.sidebar.multiselect("Filiere", sorted(df["Major_Category"].unique()))
if filieres:
    df = df[df["Major_Category"].isin(filieres)]
annees = st.sidebar.multiselect("Annee d'etude", sorted(df["Year_of_Study"].unique()))
if annees:
    df = df[df["Year_of_Study"].isin(annees)]

# Chiffres cles
c1, c2, c3 = st.columns(3)
c1.metric("Etudiants", f"{len(df):,}".replace(",", " "))
c2.metric("Progression moyenne (GPA_Delta)", f"{df['GPA_Delta'].mean():+.3f}")
c3.metric("Heures d'IA / semaine", f"{df['Weekly_GenAI_Hours'].mean():.1f} h")

# Progression : qu'est-ce qui joue ?
st.header("Qu'est-ce qui fait varier la progression ?")
colonne = st.selectbox("Comparer la progression (GPA_Delta) selon :",
                       ["Primary_Use_Case", "Institutional_Policy", "Prompt_Engineering_Skill",
                        "Major_Category", "Year_of_Study", "Profil"])
moyennes = df.groupby(colonne)["GPA_Delta"].mean().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
moyennes.plot(kind="barh", ax=ax, color="steelblue")
ax.axvline(df["GPA_Delta"].mean(), color="gray", linestyle="--", label="moyenne globale")
ax.set_xlabel("GPA_Delta moyen")
ax.legend()
st.pyplot(fig)

# Profils k-means : tableau des moyennes + nuage de points
st.header("Les 3 profils d'etudiants (k-means)")
gauche, droite = st.columns(2)

colonnes_profil = ["Weekly_GenAI_Hours", "Traditional_Study_Hours", "Perceived_AI_Dependency",
                   "Anxiety_Level_During_Exams", "Skill_Retention_Score", "GPA_Delta"]
stats = df.groupby("Profil")[colonnes_profil].mean().round(2)
stats.insert(0, "Etudiants", df["Profil"].value_counts())
gauche.write("Comportement moyen de chaque profil :")
gauche.dataframe(stats)

echantillon = df.sample(min(3000, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(7, 5))
for profil, groupe in echantillon.groupby("Profil"):
    ax.scatter(groupe["Traditional_Study_Hours"], groupe["Weekly_GenAI_Hours"],
               s=8, alpha=0.4, label=profil)
ax.set_xlabel("Heures de travail classique / semaine")
ax.set_ylabel("Heures d'IA / semaine")
ax.legend(title="Profil")
droite.pyplot(fig)
