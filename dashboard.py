import streamlit as st
import pandas as pd
import os
import zipfile
from datetime import datetime
import io
from formatador import detectar_arquivos_automaticamente, processar_nomes_txt_v3, processar_respostas_txt_v4, extrair_serie_do_nome_arquivo

# Configuração da página
st.set_page_config(
    page_title="Formatador de Dados Escolares",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 0.375rem;
    padding: 1rem;
    margin: 1rem 0;
}
.info-box {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    border-radius: 0.375rem;
    padding: 1rem;
    margin: 1rem 0;
}
.warning-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 0.375rem;
    padding: 1rem;
    margin: 1rem 0;
}
.footer {
    text-align: center;
    color: #6c757d;
    font-size: 0.8rem;
    margin-top: 3rem;
    padding: 1rem;
    border-top: 1px solid #e9ecef;
}
</style>
""", unsafe_allow_html=True)

def processar_arquivos_upload(arquivos_nomes, arquivos_respostas):
    """Processa arquivos enviados pelo usuário"""
    todos_nomes = []
    todas_respostas = []
    
    # Processar arquivos de nomes
    for arquivo in arquivos_nomes:
        # Salvar temporariamente
        with open(f"temp_{arquivo.name}", "wb") as f:
            f.write(arquivo.getbuffer())
        
        df_nomes = processar_nomes_txt_v3(f"temp_{arquivo.name}")
        if not df_nomes.empty:
            todos_nomes.append(df_nomes)
        
        # Remover arquivo temporário
        os.remove(f"temp_{arquivo.name}")
    
    # Processar arquivos de respostas
    for arquivo in arquivos_respostas:
        # Salvar temporariamente
        with open(f"temp_{arquivo.name}", "wb") as f:
            f.write(arquivo.getbuffer())
        
        df_respostas = processar_respostas_txt_v4(f"temp_{arquivo.name}")
        if not df_respostas.empty:
            todas_respostas.append(df_respostas)
        
        # Remover arquivo temporário
        os.remove(f"temp_{arquivo.name}")
    
    return todos_nomes, todas_respostas

def gerar_excel_final(df_final):
    """Gera o arquivo Excel final"""
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
    
    # Criar buffer em memória
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Aba principal
        df_final.to_excel(writer, sheet_name='Dados_Completos', index=False)
        
        # Abas por série
        series_disponiveis = df_final['Serie'].unique()
        series_ordem = ['8º Ano', '9º Ano', '1ª Série', '2ª Série']
        nomes_abas_series = {
            '8º Ano': '8_Ano',
            '9º Ano': '9_Ano', 
            '1ª Série': '1_Serie',
            '2ª Série': '2_Serie'
        }
        
        for serie in series_ordem:
            if serie in series_disponiveis:
                df_serie = df_final[df_final['Serie'] == serie]
                nome_aba = nomes_abas_series[serie]
                df_serie.to_excel(writer, sheet_name=nome_aba, index=False)
        
        # Aba de estatísticas
        stats_data = {
            'Métrica': [
                'Total de Alunos',
                'Séries Processadas',
                'Salas Identificadas',
                'Questões Processadas'
            ],
            'Valor': [
                len(df_final),
                len(df_final['Serie'].unique()),
                len(df_final['Sala'].unique()),
                len([col for col in df_final.columns if col.startswith('Q')])
            ]
        }
        pd.DataFrame(stats_data).to_excel(writer, sheet_name='Estatisticas', index=False)
        
        # Aba de resumo por sala
        resumo_salas = df_final.groupby(['Sala', 'Serie']).agg({
            'ID': 'count'
        }).rename(columns={'ID': 'Quantidade_Alunos'}).reset_index()
        resumo_salas.to_excel(writer, sheet_name='Resumo_Salas', index=False)
    
    output.seek(0)
    return output, f"Resultados_{timestamp}.xlsx"

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Formatador de Dados Escolares</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Painel de Controle")
    st.sidebar.markdown("---")
    
    # Modo de operação
    modo = st.sidebar.radio(
        "Escolha o modo de operação:",
        ["📁 Detecção Automática", "📤 Upload Manual"]
    )
    
    if modo == "📁 Detecção Automática":
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.info("🔍 **Modo Automático**: O sistema buscará automaticamente por arquivos com padrões 'nomes*.txt' e 'respostas*.txt' na pasta atual e subpastas.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Processar Arquivos Automaticamente", type="primary"):
            with st.spinner("Detectando arquivos..."):
                arquivos_nomes, arquivos_respostas = detectar_arquivos_automaticamente()
            
            if not arquivos_nomes or not arquivos_respostas:
                st.error("❌ Nenhum arquivo encontrado. Verifique se existem arquivos com 'nomes' e 'respostas' no nome.")
                return
            
            # Mostrar arquivos encontrados
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📁 Arquivos de Nomes")
                for arquivo in arquivos_nomes:
                    st.write(f"• {arquivo}")
            
            with col2:
                st.subheader("📝 Arquivos de Respostas")
                for arquivo in arquivos_respostas:
                    st.write(f"• {arquivo}")
            
            # Processar arquivos
            with st.spinner("Processando dados..."):
                todos_nomes = []
                todas_respostas = []
                
                # Processar nomes
                for arquivo in arquivos_nomes:
                    df_nomes = processar_nomes_txt_v3(arquivo)
                    if not df_nomes.empty:
                        todos_nomes.append(df_nomes)
                
                # Processar respostas
                for arquivo in arquivos_respostas:
                    df_respostas = processar_respostas_txt_v4(arquivo)
                    if not df_respostas.empty:
                        todas_respostas.append(df_respostas)
                
                if not todos_nomes or not todas_respostas:
                    st.error("❌ Erro ao processar arquivos")
                    return
                
                # Consolidar dados
                df_nomes = pd.concat(todos_nomes, ignore_index=True)
                df_respostas = pd.concat(todas_respostas, ignore_index=True)
                
                # Unificar
                df_unificado = pd.merge(
                    df_nomes,
                    df_respostas,
                    on='ID_Normalizado',
                    how='outer',
                    suffixes=('_nomes', '_respostas')
                )
                
                df_unificado['Serie'] = df_unificado['Serie_nomes'].fillna(df_unificado['Serie_respostas'])
                
                # Preparar dados finais
                colunas_basicas = ['ID_Nome', 'Nome', 'Sala', 'Serie', 'Respostas_String']
                colunas_questoes = [col for col in df_unificado.columns if col.startswith('Q')]
                colunas_questoes.sort()
                
                df_final = df_unificado.dropna(subset=['ID_Nome', 'ID_Resposta'])[colunas_basicas + colunas_questoes].copy()
                df_final = df_final.rename(columns={
                    'ID_Nome': 'ID',
                    'Nome': 'Nome',
                    'Sala': 'Sala',
                    'Serie': 'Serie',
                    'Respostas_String': 'Gabarito_Completo'
                })
                
                df_final['Sala'] = df_final['Sala'].fillna('Sala_Não_Identificada')
            
            # Mostrar resultados
            mostrar_resultados(df_final, df_unificado)
    
    else:  # Upload Manual
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.info("📤 **Modo Manual**: Faça upload dos seus arquivos de nomes e respostas.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 Arquivos de Nomes")
            arquivos_nomes = st.file_uploader(
                "Selecione os arquivos de nomes (.txt)",
                type=['txt'],
                accept_multiple_files=True,
                key="nomes"
            )
        
        with col2:
            st.subheader("📝 Arquivos de Respostas")
            arquivos_respostas = st.file_uploader(
                "Selecione os arquivos de respostas (.txt)",
                type=['txt'],
                accept_multiple_files=True,
                key="respostas"
            )
        
        if arquivos_nomes and arquivos_respostas:
            if st.button("🚀 Processar Arquivos", type="primary"):
                with st.spinner("Processando dados..."):
                    todos_nomes, todas_respostas = processar_arquivos_upload(arquivos_nomes, arquivos_respostas)
                    
                    if not todos_nomes or not todas_respostas:
                        st.error("❌ Erro ao processar arquivos")
                        return
                    
                    # Consolidar dados
                    df_nomes = pd.concat(todos_nomes, ignore_index=True)
                    df_respostas = pd.concat(todas_respostas, ignore_index=True)
                    
                    # Unificar
                    df_unificado = pd.merge(
                        df_nomes,
                        df_respostas,
                        on='ID_Normalizado',
                        how='outer',
                        suffixes=('_nomes', '_respostas')
                    )
                    
                    df_unificado['Serie'] = df_unificado['Serie_nomes'].fillna(df_unificado['Serie_respostas'])
                    
                    # Preparar dados finais
                    colunas_basicas = ['ID_Nome', 'Nome', 'Sala', 'Serie', 'Respostas_String']
                    colunas_questoes = [col for col in df_unificado.columns if col.startswith('Q')]
                    colunas_questoes.sort()
                    
                    df_final = df_unificado.dropna(subset=['ID_Nome', 'ID_Resposta'])[colunas_basicas + colunas_questoes].copy()
                    df_final = df_final.rename(columns={
                        'ID_Nome': 'ID',
                        'Nome': 'Nome',
                        'Sala': 'Sala',
                        'Serie': 'Serie',
                        'Respostas_String': 'Gabarito_Completo'
                    })
                    
                    df_final['Sala'] = df_final['Sala'].fillna('Sala_Não_Identificada')
                
                # Mostrar resultados
                mostrar_resultados(df_final, df_unificado)
    
    # Rodapé
    st.markdown('<div class="footer">Desenvolvido por Caio Murakami</div>', unsafe_allow_html=True)

def mostrar_resultados(df_final, df_unificado):
    """Mostra os resultados do processamento"""
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.success("✅ Processamento concluído com sucesso!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Estatísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total de Alunos", len(df_final))
    
    with col2:
        st.metric("📚 Séries", len(df_final['Serie'].unique()))
    
    with col3:
        st.metric("🏫 Salas", len(df_final['Sala'].unique()))
    
    with col4:
        questoes = len([col for col in df_final.columns if col.startswith('Q')])
        st.metric("❓ Questões", questoes)
    
    # Distribuição por série
    st.subheader("📊 Distribuição por Série")
    serie_counts = df_final['Serie'].value_counts()
    st.bar_chart(serie_counts)
    
    # Preview dos dados
    st.subheader("👁️ Preview dos Dados")
    st.dataframe(df_final.head(10), use_container_width=True)
    
    # Problemas encontrados
    nomes_sem_resposta = len(df_unificado[df_unificado['ID_Resposta'].isnull()])
    respostas_sem_nome = len(df_unificado[df_unificado['ID_Nome'].isnull()])
    
    if nomes_sem_resposta > 0 or respostas_sem_nome > 0:
        st.subheader("⚠️ Problemas Encontrados")
        col1, col2 = st.columns(2)
        
        with col1:
            if nomes_sem_resposta > 0:
                st.warning(f"📝 {nomes_sem_resposta} alunos sem cartão de resposta")
        
        with col2:
            if respostas_sem_nome > 0:
                st.warning(f"👤 {respostas_sem_nome} cartões sem nome correspondente")
    
    # Download do arquivo
    st.subheader("💾 Download do Resultado")
    
    excel_buffer, nome_arquivo = gerar_excel_final(df_final)
    
    st.download_button(
        label="📥 Baixar Arquivo Excel",
        data=excel_buffer,
        file_name=nome_arquivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
    
    st.info(f"📋 **Abas criadas**: Dados_Completos, 8_Ano, 9_Ano, 1_Serie, 2_Serie, Estatisticas, Resumo_Salas")

if __name__ == "__main__":
    main()