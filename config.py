import os
from dotenv import load_dotenv 

# Carrega as variáveis do arquivo .env
load_dotenv()

# Acesso ao Site
PATHTRACKER_URL = "http://portal.controlinformatica.com.br/PathTracker/"
PATHTRACKER_USERNAME = os.getenv("PATHTRACKER_USERNAME")
PATHTRACKER_PASSWORD = os.getenv("PATHTRACKER_PASSWORD")

# Configurações da extração
ABA_PADRAO = "Exclusões" # Aba do Excel
STATUS_ALVO = "Não visitado" #Status do 
TEMPO_LIMITE = 20

# Configuração do navegador
NAVEGADOR_VISIVEL = True # Se o navegador vai mostrar a automação rodando