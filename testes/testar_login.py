from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

driver = webdriver.Chrome()
wait = WebDriverWait(driver, config.TEMPO_LIMITE)

try:
    driver.maximize_window()
    driver.get(config.PATHTRACKER_URL)

    # Clica no botão Entrar
    botao_entrar = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/PathTracker/Landing/Login"]'))
    )
    botao_entrar.click()

    # Preenche usuário e senha
    campo_usuario = wait.until(
        EC.visibility_of_element_located((By.ID, "UserName"))
    )
    campo_usuario.send_keys(config.PATHTRACKER_USERNAME)

    campo_senha = wait.until(
        EC.visibility_of_element_located((By.ID, "Password"))
    )
    campo_senha.send_keys(config.PATHTRACKER_PASSWORD)

    # Envia o formulário
    formulario = campo_senha.find_element(By.XPATH, "./ancestor::form")
    formulario.find_element(By.CSS_SELECTOR, "button.btn.btn-success").click()

    # Aguarda o resultado da autenticação
    wait.until(lambda d: "/Landing/Login" not in d.current_url)

    print("Login realizado ou página de destino carregada.")
    print("URL atual:", driver.current_url)

    input("Confira o resultado no navegador. Pressione ENTER para fechar...")

finally:
    driver.quit()