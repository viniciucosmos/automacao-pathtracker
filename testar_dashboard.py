from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
import traceback
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, config.TEMPO_LIMITE)

data_rota = input(
            "Digite a data da rota (dd/mm/aaaa): "
        ).strip()

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

    ##
    
    print("\nETAPA 7: Lendo os códigos dos vendedores...")

    vendedores = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "span[data-bind='text: sellerCode']")
        )
    )

    codigos = [
        vendedor.text.strip()
        for vendedor in vendedores
        if vendedor.text.strip()
    ]

    print("Quantidade de vendedores encontrados:", len(codigos))
    print("Códigos dos vendedores:", codigos)

##
    print("\nETAPA 9: Selecionando a data da rota...")

    # Localiza o campo de data do Dashboard
    campo_data = wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "input.form-control[data-bind='value : selectedDate']"
            )
        )
    )

    # Preenche a data informada
    campo_data.clear()
    campo_data.send_keys(data_rota)

    print("Data preenchida:", campo_data.get_attribute("value"))

    # Localiza e clica no botão de atualização
    botao_atualizar = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "div.dashboard-sellers-button.filterButton button"
            )
        )
    )

    botao_atualizar.click()

    #@@

    print("Aguardando o Dashboard atualizar...")
    time.sleep(5)

    print("Data exibida após a atualização:",
        campo_data.get_attribute("value"))

    clientes_tela = driver.find_elements(
        By.CSS_SELECTOR,
        "div.table-cell[data-bind='html: sale']"
    )

    print("Elementos de clientes encontrados:", len(clientes_tela))

    com_status = 0

    for cliente in clientes_tela:
        html = cliente.get_attribute("innerHTML") or ""

        if "Não visitado" in html:
            com_status += 1

    print("Elementos contendo 'Não visitado':", com_status)

    if clientes_tela:
        print("\nAmostra do HTML do primeiro cliente:")
        print(
            (clientes_tela[0].get_attribute("innerHTML") or "")[:1000]
        )
    #@@

    print("Botão de atualização clicado.")

##  
    print("\nETAPA 8: Associando clientes aos vendedores...")

    vendedores = driver.find_elements(
        By.CSS_SELECTOR,
        "span[data-bind='text: sellerCode']"
    )

    resultado = []

    for vendedor in vendedores:
        codigo_vendedor = vendedor.get_attribute("textContent").strip()

        linha = vendedor.find_element(
            By.XPATH,
            "./ancestor::tr[1]"
        )

        clientes = linha.find_elements(
            By.CSS_SELECTOR,
            "div.table-cell[data-bind='html: sale']"
        )

        encontrados_vendedor = 0

        for cliente in clientes:
            html = cliente.get_attribute("innerHTML") or ""

            if "Não visitado" not in html:
                continue

            identificacao = cliente.find_elements(
                By.CSS_SELECTOR,
                "p.message > b"
            )

            nomes = cliente.find_elements(
                By.CSS_SELECTOR,
                "p.message > strong"
            )

            if not identificacao or not nomes:
                continue

            codigo_e_nome = identificacao[0].get_attribute(
                "textContent"
            ).strip()

            nome_comercial = nomes[0].get_attribute(
                "textContent"
            ).strip()

            partes = codigo_e_nome.split(maxsplit=1)

            if len(partes) < 2:
                continue

            resultado.append({
                "vendedor": codigo_vendedor,
                "codigo_cliente": partes[0],
                "nome_comercial": nome_comercial
            })

            encontrados_vendedor += 1

        print(
            f"Vendedor {codigo_vendedor}: "
            f"{len(clientes)} clientes na linha, "
            f"{encontrados_vendedor} não visitados."
        )

   
    print("\nTotal de clientes não visitados:", len(resultado))
    print("\nLista completa de clientes não visitados:")

    for item in resultado:
        print(
            f"Vendedor: {item['vendedor']} | "
            f"Cliente: {item['codigo_cliente']} | "
            f"Nome: {item['nome_comercial']}"
        )

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