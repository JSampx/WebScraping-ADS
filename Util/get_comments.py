from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from typing import List

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core import driver

from Models.db import Session
from Models.models import Post, Comment
from Util.login import login_in_x
from Util.settings import SCROLL_STEP


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


session = Session()
posts_list: List[Post]


def show_possible_spam():
    try:
        # Tenta localizar o botão "Mostrar provável spam"
        spam_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[contains(., 'spam')]]"
        )))
        spam_btn.click()
        print("Botão 'Mostrar provável spam' clicado ✅")
        time.sleep(1)  # dá um tempo para expandir o tweet
    except TimeoutException:
        print(f"Timeout - Botão Mostrar provável spam não encontrado")
        # Se não encontrar o botão, segue normalmente
        pass

try:
    # Conectar no Banco de dados e pegar o primeiro link
    posts_list = session.query(Post).all()
    # posts_list = session.query(Post).limit(6).all()

except Exception as e:
    print(f"Erro ao obter a conexão com o BD: {e}")


# service = Service(ChromeDriverManager().install())
# driver = login_in_x()
# driver.service = service
#
# # PID do processo do ChromeDriver
# print("PID do ChromeDriver:", service.process.pid)

# PID do navegador Chrome aberto
# print("PID do Chrome:", driver.service.process.pid)

def connect_to_x():
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"  # conecta ao Chrome já aberto

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print("Conectado ao Chrome já aberto!")
    print("Página atual:", driver.current_url)

    return driver


driver = connect_to_x()

# Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
wait = WebDriverWait(driver, 15)

# Inicializa dicionário
comment_dict = {}
i: int = 0

for post in posts_list:
    print(f'{post}\n')
    driver.get(post.link) # abre a página do post
    time.sleep(2)
    try:
        reply_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='reply']"))
        )
        try:
            reply_count = reply_button.find_element(By.XPATH, ".//span").text
            reply_count = int(reply_count)
        except ValueError:
            reply_count = 1

    except TimeoutException:
        reply_count = 1
    print("Número de respostas:", reply_count)

    driver.execute_script("document.body.style.zoom='25%'")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    show_possible_spam()
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    # # Loop para capturar todos os comentários
    driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")
    driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")
    elements: list[WebElement] = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    while i < reply_count:
        # Captura tweets visíveis
        print(f"loop: {i}")
        elements: list[WebElement] = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        print(f"entrou no loop WHILE e capturou os elementos {len(elements)}\n")

        for e in elements:
            print(f"entrou no loop FOR e capturou os elementos {len(elements)}\n")
            try:
                # Texto do tweet (ignora elementos sem texto)
                try:
                    text_divs = e.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                except TimeoutException:
                    text_divs = ""

                # Link do tweet
                link = e.find_element(By.XPATH, ".//a[contains(@href, '/status/')]").get_attribute("href")

                # Evita duplicados
                if link not in comment_dict:
                    comment_dict[link] = [text_divs, post.link]
                    print(f"[{len(comment_dict)}] {link} -> {text_divs[:100]}...")
                    driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")
                    # preview do texto
            except Exception as ex:
                print("Erro ao processar tweet:", ex)
                driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script(f"window.scrollBy(0, {SCROLL_STEP});")
        i += 1
    i = 0

print(f"\nTotal de comentários coletados: {len(comment_dict)}")



for key, value in comment_dict.items():
    try:
        comment = Comment(user=key, comment=value[0], post_id=value[1])
        session.add(comment)
        session.commit()
        print("Comentário cadastrado no BD")
        # driver.get(key)
    except Exception as e:
        session.rollback()
        print(f"Erro: {e}")
    finally:
        session.close()

