"""Dashboard Streamlit - Impact de l'IA generative sur les etudiants.

Reprend les analyses de la couche Gold du notebook (main.ipynb) :
chiffres cles, distribution des notes, facteurs de progression, progression
par groupe, distributions, et profils k-means.

Lit gold_dashboard.csv (genere par main.ipynb, section ML - Kmeans).
Lancer avec :  streamlit run app.py
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Impact IA sur les etudiants", layout="wide")

# Theme sombre pour tous les graphes matplotlib (accord avec Streamlit)
BG, FG = "#0e1117", "#fafafa"
BLEU, ROUGE = "#4c9be8", "#e06666"
mpl.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG, "axes.titlecolor": FG,
    "xtick.color": FG, "ytick.color": FG, "axes.edgecolor": FG,
    "axes.grid": True, "grid.color": "#2a2f3a", "font.size": 9,
})

NUM = ["Pre_Semester_GPA", "Weekly_GenAI_Hours", "Tool_Diversity", "Traditional_Study_Hours",
       "Perceived_AI_Dependency", "Anxiety_Level_During_Exams", "Post_Semester_GPA",
       "Skill_Retention_Score"]
CAT = ["Major_Category", "Year_of_Study", "Primary_Use_Case", "Prompt_Engineering_Skill",
       "Institutional_Policy", "Burnout_Risk_Level"]


@st.cache_data
def charger():
    df = pd.read_csv("gold_dashboard.csv")
    # Nom lisible pour chaque cluster k-means, deduit de ses caracteristiques
    moy = df.groupby("prediction")[["Weekly_GenAI_Hours", "Skill_Retention_Score"]].mean()
    dep = moy["Weekly_GenAI_Hours"].idxmax()                       # + d'heures IA
    reste = [c for c in moy.index if c != dep]
    expert = moy.loc[reste, "Skill_Retention_Score"].idxmax()      # meilleure retention
    modere = [c for c in reste if c != expert][0]
    noms = {dep: "Dependants IA", expert: "Utilisateurs experts", modere: "Usage modere"}
    df["Profil"] = df["prediction"].map(noms)
    return df


def afficher(fig):
    st.pyplot(fig)
    plt.close(fig)


try:
    df = charger()
except FileNotFoundError:
    st.error("gold_dashboard.csv introuvable. Lance d'abord la cellule d'export "
             "dans main.ipynb (section ML - Kmeans).")
    st.stop()

st.title("Impact de l'IA generative sur les etudiants")
st.caption(f"{len(df):,} etudiants - architecture medaillon (bronze/silver/gold) + k-means".replace(",", " "))

moyenne_delta = df["GPA_Delta"].mean()

t1, t2, t3, t4, t5 = st.tabs(
    ["Vue d'ensemble", "Facteurs de progression", "Progression par groupe",
     "Distributions", "Profils k-means"])

# Vue d'ensemble
with t1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Etudiants", f"{len(df):,}".replace(",", " "))
    c2.metric("GPA_Delta moyen", f"{moyenne_delta:+.3f}")
    c3.metric("Heures IA / semaine", f"{df['Weekly_GenAI_Hours'].mean():.1f} h")
    c4.metric("Retention moyenne", f"{df['Skill_Retention_Score'].mean():.1f}")

    st.subheader("Distribution de la variation de note (GPA_Delta)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(df["GPA_Delta"], bins=40, color=BLEU)
    ax.axvline(0, color="gray", linestyle="--")
    ax.axvline(moyenne_delta, color=ROUGE, linestyle="-", label=f"moyenne {moyenne_delta:+.2f}")
    ax.set_xlabel("GPA_Delta (Post - Pre)")
    ax.set_ylabel("Nombre d'etudiants")
    ax.legend()
    afficher(fig)

# Facteurs de progression
with t2:
    st.subheader("Correlation de chaque facteur avec GPA_Delta")
    corr_df = df.copy()
    corr_df["Year_of_Study_Ord"] = corr_df["Year_of_Study"].map(
        {"Freshman": 1, "Sophomore": 2, "Junior": 3, "Senior": 4, "Graduate": 5})
    corr_df["Institutional_Policy_Ord"] = corr_df["Institutional_Policy"].map(
        {"Strict_Ban": 1, "Allowed_With_Citation": 2, "Actively_Encouraged": 3})
    corr_df["Paid_Subscription_Int"] = corr_df["Paid_Subscription"].astype(str).map(
        {"True": 1, "False": 0})

    facteurs = ["Weekly_GenAI_Hours", "Traditional_Study_Hours", "Perceived_AI_Dependency",
                "Anxiety_Level_During_Exams", "Tool_Diversity", "Skill_Retention_Score",
                "Pre_Semester_GPA", "Paid_Subscription_Int", "Year_of_Study_Ord",
                "Prompt_Engineering_Skill_Ord", "Institutional_Policy_Ord"]
    corr_delta = corr_df[facteurs + ["GPA_Delta"]].corr()["GPA_Delta"].drop("GPA_Delta").sort_values()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(corr_delta.index, corr_delta.values,
            color=[ROUGE if v < 0 else BLEU for v in corr_delta])
    ax.axvline(0, color="gray")
    ax.set_xlabel("Correlation avec GPA_Delta")
    afficher(fig)

    st.subheader("Correlations entre variables numeriques")
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(df[NUM].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0,
                ax=ax, annot_kws={"size": 8})
    afficher(fig)

# Progression par groupe
with t3:
    st.subheader("GPA_Delta moyen par groupe")
    g = df.copy()
    g["Tranche_GenAI"] = pd.cut(g["Weekly_GenAI_Hours"], bins=[0, 2, 5, 10, 20, 40],
                                labels=["0-2h", "2-5h", "5-10h", "10-20h", "20-40h"],
                                include_lowest=True)
    groupes = ["Tranche_GenAI", "Primary_Use_Case", "Institutional_Policy", "Prompt_Engineering_Skill"]

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    for ax, c in zip(axes.flat, groupes):
        g.groupby(c, observed=True)["GPA_Delta"].mean().plot(kind="bar", ax=ax, color=BLEU)
        ax.axhline(moyenne_delta, color="gray", linestyle="--", label="moyenne globale")
        ax.set_title(f"par {c}")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=30)
        ax.legend(fontsize=8)
    fig.tight_layout()
    afficher(fig)

# Distributions
with t4:
    st.subheader("Variables numeriques")
    fig, axes = plt.subplots(2, 4, figsize=(15, 7))
    for ax, c in zip(axes.flat, NUM):
        ax.hist(df[c], bins=30, color=BLEU)
        ax.set_title(c, fontsize=9)
    fig.tight_layout()
    afficher(fig)

    st.subheader("Variables categorielles")
    fig, axes = plt.subplots(2, 3, figsize=(15, 7))
    for ax, c in zip(axes.flat, CAT):
        df[c].value_counts().plot(kind="bar", ax=ax, color=BLEU)
        ax.set_title(c, fontsize=9)
        ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    afficher(fig)

# Profils k-means
with t5:
    st.subheader("Profils d'etudiants (k-means, k=3)")
    cols_profil = ["Weekly_GenAI_Hours", "Traditional_Study_Hours", "Perceived_AI_Dependency",
                   "Tool_Diversity", "Anxiety_Level_During_Exams", "Skill_Retention_Score", "GPA_Delta"]
    tableau = df.groupby("Profil")[cols_profil].mean().round(2)
    tableau.insert(0, "Effectif", df["Profil"].value_counts())

    g1, g2 = st.columns(2)
    fig, ax = plt.subplots(figsize=(6, 4))
    df["Profil"].value_counts().plot(kind="bar", ax=ax, color=BLEU)
    ax.set_title("Effectif par profil")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=15)
    g1.pyplot(fig)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    df.groupby("Profil")["GPA_Delta"].mean().plot(kind="bar", ax=ax, color=BLEU)
    ax.axhline(moyenne_delta, color="gray", linestyle="--", label="moyenne globale")
    ax.set_title("GPA_Delta moyen par profil")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=15)
    ax.legend(fontsize=8)
    g2.pyplot(fig)
    plt.close(fig)

    st.markdown("**Caracteristiques moyennes par profil**")
    st.dataframe(tableau, use_container_width=True)
