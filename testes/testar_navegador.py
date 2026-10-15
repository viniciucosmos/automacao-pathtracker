from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config

options = Options()

if config.NAVEGADOR_VISIVEL:
    options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    driver.get(config.PATHTRACKER_URL)

    print("Título da página:", driver.title)
    print("URL atual:", driver.current_url)

    input("Confira o navegador. Pressione ENTER para fechar...")

finally:
    driver.quit()