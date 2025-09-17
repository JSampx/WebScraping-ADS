import pandas as pd
from sqlalchemy import text

from Models.db import engine
from Util.settings import URI_PATH


def export_to_csv():
    query = """
            SELECT p.id, p.nome_portal, p.texto_postagem, u.comment 
            FROM posts p JOIN comments u 
                              ON p.link = u.post_id;
    """

    # executa e transforma em DataFrame
    df = pd.read_sql(text(query), engine)

    # exporta para CSV
    df.to_csv(f"xposts-{URI_PATH}.csv", index=False, encoding="utf-8")

export_to_csv()