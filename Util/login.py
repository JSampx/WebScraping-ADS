import os

from Util.settings import ROOT_PATH_LOGIN, EMAIL_ACCOUNT, USER_ACCOUNT, USER_PASSWORD

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# função de acesso ao x
def login_in_x():
    # Chrome options5
    chrome_options = Options()
    #chrome_options.debugger_address = "127.0.0.1:9222"

    if os.name == "posix": # verifica se o Sistema Operacional é Linux
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-debugging-port=9222")
        # chrome_options.add_argument("--headless=new")  # use se não quiser abrir janela

    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(ROOT_PATH_LOGIN)

    wait = WebDriverWait(driver, 15)

    # 1. Campo de e-mail/usuário
    input_login = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
    input_login.clear()
    input_login.send_keys(EMAIL_ACCOUNT)

    submit_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[normalize-space(text())='Avançar' or normalize-space(text())='Next']]"
    )))
    submit_btn.click()

    # 2. Passo extra (às vezes aparece pedindo usuário/telefone)
    try:
        input_acc = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']"
        )))
        input_acc.clear()
        input_acc.send_keys(USER_ACCOUNT)

        submit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[normalize-space(text())='Avançar' or normalize-space(text())='Next']]"
        )))
        submit_btn.click()
    except:
        print("Passo extra de confirmação não apareceu")

    # 3. Campo de senha
    input_psw = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='current-password']")))
    input_psw.clear()
    input_psw.send_keys(USER_PASSWORD)

    # 4. Botão final de login
    submit_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"
    )))
    submit_btn.click()


    time.sleep(1)  # só para ver o resultado antes de fechar

    return driver