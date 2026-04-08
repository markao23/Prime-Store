import os 
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("O DISCORD_TOKEN não foi encontrado no arquivo .env!")

# --- POSTGRESQL ---
# Usamos os.getenv("VARIAVEL", "valor_padrao") para definir um fallback caso falte algo
DB_HOST = os.getenv("DB_HOST", "localhost") 
DB_PORT = os.getenv("DB_PORT", "5432")      
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Validação de segurança: impede que o bot inicie se faltar a senha ou o usuário
if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError("ERRO: Faltam credenciais do Banco de Dados no arquivo .env!")

# Montando a URL de Conexão (Padrão: postgresql://usuario:senha@host:porta/banco)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
