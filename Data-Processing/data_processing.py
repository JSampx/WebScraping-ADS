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

df = pd.read_csv("../Models/xposts-g1.csv", delimiter="|")

df.dropna(inplace=True)
print(df.info())

df['texto_postagem'] = df['texto_postagem'].str.replace(r"\w+\.\w+\/\w+|#\w+", "", regex=True)
df["comment"] = df["comment"].str.lower().str.replace(r"\w+\.\w+\/\w+|#\w+|\n|@\w+|([!?.:,;])\1+|\s+", " ", regex=True).str.strip()
df["sentimento"] =  df["comment"].apply(sentiment_analysis)

df.to_csv("xposts-processed.csv", sep="|", index=False)