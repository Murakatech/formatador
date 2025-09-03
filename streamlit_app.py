# Arquivo principal para deploy no Streamlit Cloud
# Este arquivo é um alias para dashboard.py para compatibilidade com Streamlit Cloud

import sys
import os

# Adiciona o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa e executa o dashboard principal
if __name__ == "__main__":
    # Executa o dashboard principal
    exec(open('dashboard.py').read())