from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
import traceback

driver = webdriver.Chrome()
wait = WebDriverWait(driver, config.TEMPO_LIMITE)

try:
    print("ETAPA 1: Abrindo o portal...")
    driver.maximize_window()
    driver.get(config.PATHTRACKER_URL)

    print("ETAPA 2: Acessando o login...")
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/PathTracker/Landing/Login"]')
        )
    ).click()

    print("ETAPA 3: Preenchendo as credenciais...")
    wait.until(
        EC.visibility_of_element_located((By.ID, "UserName"))
    ).send_keys(config.PATHTRACKER_USERNAME)

    campo_senha = wait.until(
        EC.visibility_of_element_located((By.ID, "Password"))
    )
    campo_senha.send_keys(config.PATHTRACKER_PASSWORD)

    campo_senha.find_element(
        By.XPATH, "./ancestor::form"
    ).find_element(
        By.CSS_SELECTOR, "button.btn.btn-success"
    ).click()

    print("ETAPA 4: Aguardando o login...")
    wait.until(lambda d: "/Landing/Login" not in d.current_url)

    print("URL após login:", driver.current_url)

    print("ETAPA 5: Localizando o menu Vendas...")

    menu_vendas = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Vendas")
        )
    )

    menu_vendas.click()

    print("URL após clicar em Vendas:", driver.current_url)

    print("Links disponíveis após clicar em Vendas:")
    for link in driver.find_elements(By.TAG_NAME, "a"):
        texto = link.text.strip()
        href = link.get_attribute("href")

        if texto or href:
            print(f"Texto: {texto} | Link: {href}")


    print("ETAPA 6: Localizando o Dashboard visível...")

    links_dashboard = driver.find_elements(
        By.XPATH,
        "//a[@href='/PathTracker/Sellers/SellersDashboard']"
    )

    dashboard = next(
        (link for link in links_dashboard if link.is_displayed()),
        None
    )

    if dashboard is None:
        raise Exception("Nenhum link visível do Dashboard foi encontrado.")

    print("Link visível encontrado:", dashboard.rect)

    # Clica no link visível, sem procurar novamente por outro elemento.
    dashboard.click()

    # Confirma que a navegação aconteceu.
    wait.until(
        lambda d: "SellersDashboard" in d.current_url
    )

    print("Dashboard aberto com sucesso!")
    print("URL atual:", driver.current_url)

    input("Confira o dashboard. Pressione ENTER para fechar...")
    
except Exception:
    print("\nERRO DURANTE A EXECUÇÃO:")
    traceback.print_exc()

    print("\nURL no momento do erro:", driver.current_url)
    print("Título:", driver.title)

    input(
        "\nO navegador permanecerá aberto para inspeção. "
        "Pressione ENTER para fechar..."
    )

finally:
    driver.quit()