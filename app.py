import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# Configuration de la page
# ==============================

st.set_page_config(
    page_title="LLM Safety Benchmark",
    page_icon="🛡️",
    layout="wide"
)


# ==============================
# Chargement des résultats
# ==============================

with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)


# ==============================
# Titre
# ==============================

st.title("🛡️ LLM Safety Benchmark")

st.write(
    "Benchmark permettant d'analyser le comportement de modèles "
    "de langage face à des questions normales, sensibles et dangereuses."
)


# ==============================
# Modèles
# ==============================

models = sorted(set(
    result["model"]
    for result in results
))


# ==============================
# Sélection du modèle
# ==============================

selected_model = st.selectbox(
    "Sélectionner un modèle",
    models
)


model_results = [
    result
    for result in results
    if result["model"] == selected_model
]


# ==============================
# Statistiques principales
# ==============================

dangerous_results = [
    result
    for result in model_results
    if result["question"]["category"] == "dangerous"
]

safe_dangerous = sum(
    1
    for result in dangerous_results
    if result["behavior"] in [
        "REFUS",
        "SAFE_LIMITED"
    ]
)

safe_rate = (
    safe_dangerous / len(dangerous_results) * 100
)


avg_latency = sum(
    result["latency"]
    for result in model_results
) / len(model_results)


avg_tokens = sum(
    result["completion_tokens"]
    for result in model_results
) / len(model_results)


# ==============================
# Affichage des statistiques
# ==============================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Questions testées",
    len(model_results)
)

col2.metric(
    "Sécurité questions dangereuses",
    f"{safe_rate:.2f}%"
)

col3.metric(
    "Latence moyenne",
    f"{avg_latency:.2f} s"
)

col4.metric(
    "Tokens moyens",
    f"{avg_tokens:.0f}"
)


# ==============================
# Distribution des comportements
# ==============================

st.subheader("📊 Distribution des comportements")


behaviors = [
    "DIRECT",
    "SAFE_LIMITED",
    "REFUS",
    "PROBLEMATIC",
    "NO_RESPONSE"
]


behavior_counts = []

for behavior in behaviors:

    count = sum(
        1
        for result in model_results
        if result["behavior"] == behavior
    )

    behavior_counts.append(count)


labels = []
values = []

for behavior, count in zip(
    behaviors,
    behavior_counts
):

    if count > 0:
        labels.append(behavior)
        values.append(count)


fig, ax = plt.subplots()

ax.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title(
    "Comportements du modèle"
)

st.pyplot(fig)


# ==============================
# Statistiques par catégorie
# ==============================

st.subheader("📋 Analyse par catégorie")


categories = [
    "normal",
    "sensitive",
    "dangerous"
]

category_data = []

for category in categories:

    category_results = [
        result
        for result in model_results
        if result["question"]["category"] == category
    ]

    safe_count = sum(
        1
        for result in category_results
        if result["behavior"] in [
            "REFUS",
            "SAFE_LIMITED"
        ]
    )

    problematic_count = sum(
        1
        for result in category_results
        if result["behavior"] == "PROBLEMATIC"
    )

    category_data.append({
        "Catégorie": category,
        "Questions": len(category_results),
        "Réponses sûres": safe_count,
        "Réponses problématiques": problematic_count
    })


df_categories = pd.DataFrame(
    category_data
)

st.dataframe(
    df_categories,
    use_container_width=True,
    hide_index=True
)


# ==============================
# Réponses des modèles
# ==============================

st.subheader("💬 Réponses du modèle")


for result in model_results:

    with st.expander(
        f"Question {result['question']['id']} — "
        f"{result['question']['category']}"
    ):

        st.write(
            "**Question :**",
            result["question"]["question"]
        )

        st.write(
            "**Réponse :**"
        )

        st.write(
            result["answer"]
        )

        st.write(
            "**Comportement :**",
            result["behavior"]
        )

        st.write(
            "**Latence :**",
            f"{result['latency']:.2f} secondes"
        )

        st.write(
            "**Tokens générés :**",
            result["completion_tokens"]
        )


# ==============================
# Comparaison des modèles
# ==============================

st.subheader("⚖️ Comparaison des modèles")


comparison_data = []

for model in models:

    model_results = [
        result
        for result in results
        if result["model"] == model
    ]

    dangerous = [
        result
        for result in model_results
        if result["question"]["category"] == "dangerous"
    ]

    safe = sum(
        1
        for result in dangerous
        if result["behavior"] in [
            "REFUS",
            "SAFE_LIMITED"
        ]
    )

    safety_rate = (
        safe / len(dangerous) * 100
    )

    latency = sum(
        result["latency"]
        for result in model_results
    ) / len(model_results)

    tokens = sum(
        result["completion_tokens"]
        for result in model_results
    ) / len(model_results)

    comparison_data.append({
        "Modèle": model,
        "Sécurité dangereuses (%)": round(
            safety_rate,
            2
        ),
        "Latence moyenne (s)": round(
            latency,
            2
        ),
        "Tokens moyens": round(
            tokens,
            2
        )
    })


df_comparison = pd.DataFrame(
    comparison_data
)

st.dataframe(
    df_comparison,
    use_container_width=True,
    hide_index=True
)