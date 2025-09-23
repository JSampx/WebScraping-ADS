import pandas as pd
import matplotlib.pyplot as plt
import textwrap

df = pd.read_csv("../Data-Processing/xposts-processed.csv", sep="|")
contagem_sentimentos = df.groupby("texto_postagem")["sentimento"].value_counts().unstack(fill_value=0)

# Itera por cada postagem
for postagem, row in contagem_sentimentos.iterrows():
    # row é uma Series: POSITIVO, NEUTRO, NEGATIVO
    titulo_formatado = textwrap.fill(postagem, width=40)
    row = row[['POSITIVO', 'NEUTRO', 'NEGATIVO']]  # garante a ordem

    plt.figure(figsize=(6, 4))
    plt.bar(row.index, row.values, color=['tab:green', 'tab:gray', 'tab:red'])
    plt.title(titulo_formatado)
    plt.ylabel('Número de comentários')
    plt.xlabel('Sentimento')
    plt.tight_layout()
    plt.savefig(f"../Data-Analysis/exported_charts/{postagem[:20]}.png")
    plt.show()
