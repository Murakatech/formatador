# Dockerfile para Formatador de Dados Escolares
# Permite deploy em qualquer plataforma que suporte containers

FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências Python
RUN pip3 install -r requirements.txt

# Copia todos os arquivos da aplicação
COPY . .

# Expõe a porta que o Streamlit usa
EXPOSE 8501

# Define variáveis de ambiente
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true

# Comando de verificação de saúde
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Comando para executar a aplicação
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]