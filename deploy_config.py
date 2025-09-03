# Configurações para deploy em diferentes plataformas de nuvem
# Formatador de Dados Escolares - Deploy Configuration

import os
import streamlit as st

def configure_for_cloud_deployment():
    """
    Configura a aplicação para execução em nuvem
    """
    # Configurações para diferentes plataformas
    
    # Detecta a plataforma de deploy
    platform = detect_platform()
    
    # Configurações específicas por plataforma
    if platform == "streamlit_cloud":
        configure_streamlit_cloud()
    elif platform == "heroku":
        configure_heroku()
    elif platform == "railway":
        configure_railway()
    elif platform == "render":
        configure_render()
    else:
        configure_default()

def detect_platform():
    """
    Detecta a plataforma de deploy baseada em variáveis de ambiente
    """
    if os.getenv('STREAMLIT_CLOUD'):
        return "streamlit_cloud"
    elif os.getenv('DYNO'):
        return "heroku"
    elif os.getenv('RAILWAY_ENVIRONMENT'):
        return "railway"
    elif os.getenv('RENDER'):
        return "render"
    else:
        return "local"

def configure_streamlit_cloud():
    """
    Configurações específicas para Streamlit Cloud
    """
    st.set_page_config(
        page_title="Formatador de Dados Escolares - Online",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/seu-usuario/formatador-dados',
            'Report a bug': 'https://github.com/seu-usuario/formatador-dados/issues',
            'About': "# Formatador de Dados Escolares\nVersão Online - Desenvolvido por Caio Murakami"
        }
    )

def configure_heroku():
    """
    Configurações específicas para Heroku
    """
    # Configurações para Heroku
    port = int(os.environ.get("PORT", 8501))
    return {
        'server.port': port,
        'server.address': '0.0.0.0',
        'server.headless': True
    }

def configure_railway():
    """
    Configurações específicas para Railway
    """
    port = int(os.environ.get("PORT", 8501))
    return {
        'server.port': port,
        'server.address': '0.0.0.0',
        'server.headless': True
    }

def configure_render():
    """
    Configurações específicas para Render
    """
    port = int(os.environ.get("PORT", 8501))
    return {
        'server.port': port,
        'server.address': '0.0.0.0',
        'server.headless': True
    }

def configure_default():
    """
    Configurações padrão para execução local ou outras plataformas
    """
    return {
        'server.port': 8501,
        'server.address': '0.0.0.0',
        'server.headless': True
    }

def get_base_url():
    """
    Retorna a URL base da aplicação baseada na plataforma
    """
    platform = detect_platform()
    
    if platform == "streamlit_cloud":
        # URL será fornecida pelo Streamlit Cloud
        return "https://seu-app.streamlit.app"
    elif platform == "heroku":
        app_name = os.getenv('HEROKU_APP_NAME', 'formatador-dados')
        return f"https://{app_name}.herokuapp.com"
    elif platform == "railway":
        return os.getenv('RAILWAY_STATIC_URL', 'https://formatador-dados.railway.app')
    elif platform == "render":
        return os.getenv('RENDER_EXTERNAL_URL', 'https://formatador-dados.onrender.com')
    else:
        return "http://localhost:8501"

def show_deployment_info():
    """
    Mostra informações sobre o deploy atual
    """
    platform = detect_platform()
    base_url = get_base_url()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Informações de Deploy")
    st.sidebar.info(f"**Plataforma**: {platform.title()}")
    st.sidebar.info(f"**URL**: {base_url}")
    
    if platform != "local":
        st.sidebar.success("✅ Aplicação rodando online!")
        st.sidebar.markdown(
            f"🔗 **Compartilhe este link**: [{base_url}]({base_url})"
        )
    else:
        st.sidebar.warning("⚠️ Executando localmente")

# Configurações de segurança para produção
def configure_security():
    """
    Configurações de segurança para ambiente de produção
    """
    # Desabilita algumas funcionalidades em produção
    if detect_platform() != "local":
        # Configurações de segurança
        os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
        os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'true'
        
# Inicializa as configurações
if __name__ == "__main__":
    configure_for_cloud_deployment()
    configure_security()