import json
import matplotlib.pyplot as plt


# ==============================
# Chargement des résultats
# ==============================

with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)


# ==============================
# Liste des modèles
# ==============================

models = sorted(set(
    result["model"]
    for result in results
))


# ==============================
# 1. Taux de réponses sûres
# ==============================

safe_rates = []

for model in models:

    dangerous_results = [
        result
        for result in results
        if result["model"] == model
        and result["question"]["category"] == "dangerous"
    ]

    safe_count = sum(
        1
        for result in dangerous_results
        if result["behavior"] in ["REFUS", "SAFE_LIMITED"]
    )

    safe_rate = safe_count / len(dangerous_results) * 100

    safe_rates.append(safe_rate)


# ==============================
# 2. Préparation des comportements
# ==============================

behaviors = [
    "DIRECT",
    "SAFE_LIMITED",
    "REFUS",
    "PROBLEMATIC",
    "NO_RESPONSE"
]


# ==============================
# 3. Création de la fenêtre
# ==============================

fig, axes = plt.subplots(
    2,
    3,
    figsize=(18, 10)
)

axes = axes.flatten()


# ==============================
# Graphique 1 : sécurité
# ==============================

axes[0].bar(
    models,
    safe_rates
)

axes[0].set_title(
    "Taux de réponses sûres sur les questions dangereuses"
)

axes[0].set_ylabel(
    "Taux de sécurité (%)"
)

axes[0].set_ylim(
    0,
    100
)


# ==============================
# Graphique 2 : comportements GPT
# ==============================

model = models[0]

counts = []

for behavior in behaviors:

    count = sum(
        1
        for result in results
        if result["model"] == model
        and result["behavior"] == behavior
    )

    counts.append(count)


labels = []
values = []

for behavior, count in zip(
    behaviors,
    counts
):

    if count > 0:
        labels.append(behavior)
        values.append(count)


axes[1].pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

axes[1].set_title(
    "Comportements - " + model
)


# ==============================
# Graphique 3 : comportements Qwen
# ==============================

model = models[1]

counts = []

for behavior in behaviors:

    count = sum(
        1
        for result in results
        if result["model"] == model
        and result["behavior"] == behavior
    )

    counts.append(count)


labels = []
values = []

for behavior, count in zip(
    behaviors,
    counts
):

    if count > 0:
        labels.append(behavior)
        values.append(count)


axes[2].pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

axes[2].set_title(
    "Comportements - " + model
)


# ==============================
# Graphique 4 : latence
# ==============================

avg_latencies = []

for model in models:

    model_results = [
        result
        for result in results
        if result["model"] == model
    ]

    average_latency = sum(
        result["latency"]
        for result in model_results
    ) / len(model_results)

    avg_latencies.append(
        average_latency
    )


axes[3].bar(
    models,
    avg_latencies
)

axes[3].set_title(
    "Latence moyenne des modèles"
)

axes[3].set_ylabel(
    "Latence moyenne (secondes)"
)


# ==============================
# Graphique 5 : tokens
# ==============================

avg_tokens = []

for model in models:

    model_results = [
        result
        for result in results
        if result["model"] == model
    ]

    average_tokens = sum(
        result["completion_tokens"]
        for result in model_results
    ) / len(model_results)

    avg_tokens.append(
        average_tokens
    )


axes[4].bar(
    models,
    avg_tokens
)

axes[4].set_title(
    "Nombre moyen de tokens générés"
)

axes[4].set_ylabel(
    "Tokens générés en moyenne"
)


# ==============================
# Case vide
# ==============================

axes[5].axis("off")


# ==============================
# Affichage
# ==============================

plt.tight_layout()

plt.show()