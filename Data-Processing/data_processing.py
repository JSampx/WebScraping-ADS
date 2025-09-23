import pandas as pd
from LeIA import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def sentiment_analysis(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score > 0.5:
        return "POSITIVO"
    elif 0.5 >= score >= -0.5:
        return "NEUTRO"
    else:
        return "NEGATIVO"
# Leitura do arquivo csv
df = pd.read_csv("../Models/xposts-g1.csv", delimiter="|")

# retira linhas vazias
df.dropna(inplace=True)
print(df.info())

# limpeza do texto, retirando espaços, identações e caracteres extras
df['texto_postagem'] = df['texto_postagem'].str.replace(r"\w+\.\w+\/\w+|#\w+", "", regex=True)
df["comment"] = df["comment"].str.lower().str.replace(r"\w+\.\w+\/\w+|#\w+|\n|@\w+|([!?.:,;])\1+|\s+", " ", regex=True).str.strip()
df["sentimento"] =  df["comment"].apply(sentiment_analysis)

# Salva o dataframe em novo arquivo com coluna sentimento
df.to_csv("xposts-processed.csv", sep="|", index=False)