from Models.db import Session
from Models.models import Post
from Util.settings import ROOT_PATH, URI_PATH, SCROLL_STEP, PERSIST_TWT
from Util.login import login_in_x

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

driver = login_in_x()


# Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver.get(f"{ROOT_PATH}{URI_PATH}")
time.sleep(5)

# Inicializa dicionário
twt_dict = {}
# Loop para capturar 30 tweets
while len(twt_dict) < 30:
    tweet_xpath = "//article[@data-testid='tweet']"
    tweet_xpath_text = ".//div[@data-testid='tweetText']"
    tweet_xpath_href = ".//a[contains(@href, '/status/')]"

    # Rola a página
    driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")
    time.sleep(1)

    # Captura tweets visíveis
    elements = (driver.find_elements(By.XPATH, tweet_xpath))

    for e in elements:
        try:
            # Texto do tweet (ignora elementos sem texto)
            try:
                text_divs = e.find_element(By.XPATH, tweet_xpath_text).text
            except Exception as e:
                print(f"Erro: {e}")
                text_divs = ""

            # Link do tweet
            link = (e.find_element(By.XPATH, tweet_xpath_href)
                    .get_attribute("href"))

            # Evita duplicados
            if link not in twt_dict:
                twt_dict[link] = text_divs
                # preview do texto
                print(f"[{len(twt_dict)}] {link} -> {text_divs[:50]}...")
        except Exception as ex:
            print("Erro ao processar tweet:", ex)

print(f"\nTotal de tweets coletados: {len(twt_dict)}")


session = Session()

if PERSIST_TWT:
    for key, value in twt_dict.items():
        try:
            post = Post(link=key, nome_portal=URI_PATH, texto_postagem=value)
            session.add(post)
            session.commit()
            print("Tweet cadastrado no BD")
        except Exception as e:
            session.rollback()
            print(f"Erro: {e}")
        finally:
            session.close()
