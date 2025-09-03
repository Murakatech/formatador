import pandas as pd
import re
import os
import glob
from pathlib import Path
from datetime import datetime

def detectar_arquivos_automaticamente():
    """
    Detecta automaticamente todos os arquivos de nomes e respostas na pasta atual e subpastas.
    """
    print("🔍 DETECTANDO ARQUIVOS AUTOMATICAMENTE...")
    
    # Padrões para detectar arquivos
    padroes_nomes = ['**/nomes*.txt', '**/nome*.txt', 'nomes*.txt', 'nome*.txt']
    padroes_respostas = ['**/respostas*.txt', '**/resposta*.txt', 'respostas*.txt', 'resposta*.txt']
    
    arquivos_nomes = []
    arquivos_respostas = []
    
    # Buscar arquivos de nomes
    for padrao in padroes_nomes:
        arquivos_nomes.extend(glob.glob(padrao, recursive=True))
    
    # Buscar arquivos de respostas
    for padrao in padroes_respostas:
        arquivos_respostas.extend(glob.glob(padrao, recursive=True))
    
    # Remover duplicatas e ordenar
    arquivos_nomes = sorted(list(set(arquivos_nomes)))
    arquivos_respostas = sorted(list(set(arquivos_respostas)))
    
    print(f"📁 Arquivos de nomes encontrados: {len(arquivos_nomes)}")
    for arquivo in arquivos_nomes:
        print(f"   - {arquivo}")
    
    print(f"📁 Arquivos de respostas encontrados: {len(arquivos_respostas)}")
    for arquivo in arquivos_respostas:
        print(f"   - {arquivo}")
    
    return arquivos_nomes, arquivos_respostas

def extrair_serie_do_nome_arquivo(nome_arquivo):
    """
    Extrai a série do nome do arquivo (1°, 2°, 8°, 9°, 8th grade, etc.)
    """
    nome_arquivo = nome_arquivo.lower()
    
    # Padrões para diferentes formatos de série
    padroes = [
        (r'1[°ª]|1\s*serie', '1ª Série'),
        (r'2[°ª]|2\s*serie', '2ª Série'),
        (r'8[°ª]|8\s*serie|8th\s*grade', '8º Ano'),
        (r'9[°ª]|9\s*serie', '9º Ano')
    ]
    
    for padrao, serie in padroes:
        if re.search(padrao, nome_arquivo):
            return serie
    
    return 'Série não identificada'

# Função de gráficos removida conforme solicitação do usuário

def processar_nomes_txt_v3(file_path):
    """
    Processa o arquivo de nomes, extraindo Código, Nome e Sala (incluindo todas as salas especificadas).
    Agora com suporte a detecção automática de série.
    """
    dados_nomes = []
    sala_atual = ""
    serie_arquivo = extrair_serie_do_nome_arquivo(file_path)
    
    print(f"\n📖 Processando nomes: {file_path} ({serie_arquivo})")
    
    # Padrões de salas suportadas
    padroes_salas = [
        r'(\d+CM)\s*-\s*9º\s*Ano',
        r'(\d+DM)\s*-\s*1ª\s*Série',
        r'(\d+EM)\s*-\s*2ª\s*Série',
        r'(\d+AM)\s*-\s*8º\s*ano',
        r'(\d+AM)\s*-\s*8º\s*Ano',
        r'(\d+CM)\s*-\s*9º\s*Ano',
        r'(\d+DM)\s*-\s*1ª\s*Série',
        r'(\d+EM)\s*-\s*2ª\s*Série',
        # Padrões mais simples para compatibilidade
        r'(\d+[ACDE]M)',
        r'(\d+EM)'
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                
                # Procura por linhas de Sala usando todos os padrões
                sala_encontrada = False
                for padrao in padroes_salas:
                    sala_match = re.search(padrao, linha, re.IGNORECASE)
                    if sala_match:
                        sala_atual = sala_match.group(1).upper()
                        print(f"🏫 Sala encontrada: {sala_atual}")
                        sala_encontrada = True
                        break
                
                if sala_encontrada:
                    continue
                
                # Procura por linhas de cabeçalho
                if 'Código Aluno' in linha or 'Código' in linha:
                    continue
                
                # Procura por linhas com o código do aluno
                if re.match(r'^\d+\.\d+', linha):
                    parts = linha.split('\t')
                    codigo = parts[0].strip()
                    # A coluna do nome pode variar, vamos encontrar a mais provável
                    nome_parts = [p.strip() for p in parts if p.strip() and not re.match(r'^\d+\.?\d*$', p)]
                    if nome_parts:
                        nome = nome_parts[0]
                        if codigo and nome:
                            # Remover pontos - só números
                            codigo_sem_ponto = codigo.replace('.', '')
                            dados_nomes.append({
                                'ID_Nome': codigo_sem_ponto,
                                'Nome': nome,
                                'Sala': sala_atual if sala_atual else 'Sala_Não_Identificada',
                                'Serie': serie_arquivo,
                                'ID_Normalizado': codigo_sem_ponto.strip(),
                                'Arquivo_Origem': file_path
                            })
        
        df_nomes = pd.DataFrame(dados_nomes)
        print(f"✅ nomes.txt processado: {len(df_nomes)} registros")
        
        # Mostrar resumo das salas
        if not df_nomes.empty:
            print(f"📊 Resumo das salas encontradas:")
            salas_count = df_nomes['Sala'].value_counts()
            for sala, count in salas_count.items():
                print(f"   {sala}: {count} alunos")
        
        return df_nomes
        
    except Exception as e:
        print(f"❌ Erro ao processar nomes.txt: {e}")
        return pd.DataFrame()

def processar_respostas_txt_v4(file_path):
    """
    Processa o arquivo de respostas, extraindo o código e separando cada resposta.
    Agora com suporte a detecção automática de série.
    """
    dados_respostas = []
    max_questoes = 150  # AJUSTE AQUI: Máximo de questões a processar
    serie_arquivo = extrair_serie_do_nome_arquivo(file_path)
    
    print(f"\n📝 Processando respostas: {file_path} ({serie_arquivo})")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    # Padrão modificado para incluir asteriscos e outros caracteres
                    match = re.search(r'N\s*(\d+)\s*([A-E*]+)', linha)
                    if match:
                        codigo_completo = match.group(1).strip()
                        respostas_string = match.group(2).strip()
                        
                        # Normalizar código (remove último dígito e zeros à esquerda)
                        codigo_normalizado = codigo_completo[:-1].lstrip('0')
                        
                        # Separar cada resposta individual PRESERVANDO ASTERISCOS
                        respostas_lista = list(respostas_string)
                        
                        # Criar dicionário com todas as respostas
                        registro = {
                            'ID_Resposta': codigo_completo,
                            'Respostas_String': respostas_string,
                            'ID_Normalizado': codigo_normalizado,
                            'Serie': serie_arquivo,
                            'Total_Questoes_Real': len(respostas_lista),  # Quantas questões realmente tem
                            'Arquivo_Origem': file_path
                        }
                        
                        # Adicionar cada resposta como uma coluna (Q001, Q002, Q003, ...) ATÉ O MÁXIMO
                        # PRESERVANDO ASTERISCOS nas posições exatas
                        for i in range(1, max_questoes + 1):
                            if i <= len(respostas_lista):
                                # Se existe a resposta, usa ela (incluindo asteriscos)
                                registro[f'Q{i:03d}'] = respostas_lista[i-1]
                            else:
                                # Se não existe, deixa vazio
                                registro[f'Q{i:03d}'] = ''
                        
                        dados_respostas.append(registro)
        
        df_respostas = pd.DataFrame(dados_respostas)
        print(f"✅ respostas.txt processado: {len(df_respostas)} registros")
        
        if not df_respostas.empty:
            # Mostrar estatísticas das questões
            questoes_reais = df_respostas['Total_Questoes_Real'].max()
            questoes_min = df_respostas['Total_Questoes_Real'].min()
            questoes_media = round(df_respostas['Total_Questoes_Real'].mean(), 1)
            
            print(f"📝 Questões encontradas:")
            print(f"   Máximo: {questoes_reais} questões")
            print(f"   Mínimo: {questoes_min} questões") 
            print(f"   Média: {questoes_media} questões")
            print(f"   Colunas criadas: Q001 até Q{max_questoes:03d} (máximo configurado: {max_questoes})")
            
            if questoes_reais > max_questoes:
                print(f"⚠️  ATENÇÃO: Alguns cartões têm mais questões ({questoes_reais}) do que o configurado ({max_questoes})")
                print(f"   Para processar todas, altere 'max_questoes = {questoes_reais}' no código")
        
        return df_respostas
        
    except Exception as e:
        print(f"❌ Erro ao processar respostas.txt: {e}")
        return pd.DataFrame()

# Função separar_por_salas removida conforme solicitação do usuário

def main():
    print("🚀 FORMATADOR UNIFICADO - DETECÇÃO AUTOMÁTICA E ANÁLISES AVANÇADAS")
    print("=" * 80)
    
    # Detectar arquivos automaticamente
    arquivos_nomes, arquivos_respostas = detectar_arquivos_automaticamente()
    
    if not arquivos_nomes or not arquivos_respostas:
        print("❌ Nenhum arquivo encontrado. Verifique se existem arquivos com 'nomes' e 'respostas' no nome.")
        return
    
    # Processar todos os arquivos
    todos_nomes = []
    todas_respostas = []
    
    # Processar arquivos de nomes
    for arquivo in arquivos_nomes:
        df_nomes = processar_nomes_txt_v3(arquivo)
        if not df_nomes.empty:
            todos_nomes.append(df_nomes)
    
    # Processar arquivos de respostas
    for arquivo in arquivos_respostas:
        df_respostas = processar_respostas_txt_v4(arquivo)
        if not df_respostas.empty:
            todas_respostas.append(df_respostas)
    
    if not todos_nomes or not todas_respostas:
        print("❌ Erro ao processar arquivos")
        return
    
    # Consolidar todos os dados
    print("\n🔗 CONSOLIDANDO TODOS OS DADOS...")
    df_nomes = pd.concat(todos_nomes, ignore_index=True)
    df_respostas = pd.concat(todas_respostas, ignore_index=True)
    
    if df_nomes.empty or df_respostas.empty:
        print("❌ Erro ao processar arquivos")
        return

    # Unificação dos dados
    print("\n🔗 UNIFICANDO OS DADOS...")
    df_unificado = pd.merge(
        df_nomes, 
        df_respostas, 
        on='ID_Normalizado', 
        how='outer',
        suffixes=('_nomes', '_respostas')
    )
    
    # Limpar e organizar dados de série
    df_unificado['Serie'] = df_unificado['Serie_nomes'].fillna(df_unificado['Serie_respostas'])
    
    # Estatísticas
    print("\n📊 GERANDO O RESUMO")
    nomes_sem_resposta = df_unificado[df_unificado['ID_Resposta'].isnull()]['ID_Nome'].count()
    respostas_sem_nome = df_unificado[df_unificado['ID_Nome'].isnull()]['ID_Resposta'].count()
    total_unificados = df_unificado.dropna(subset=['ID_Nome', 'ID_Resposta']).shape[0]

    print(f"✅ Registros unificados com sucesso: {total_unificados}")
    print(f"❌ Nomes sem cartão de resposta: {nomes_sem_resposta}")
    print(f"❌ Cartões de resposta sem nome: {respostas_sem_nome}")
    
    # Preparar o DataFrame final
    print("\n🎯 PREPARANDO ARQUIVO FINAL...")
    
    # Colunas básicas
    colunas_basicas = ['ID_Nome', 'Nome', 'Sala', 'Serie', 'Respostas_String']
    
    # Colunas das questões (agora com 3 dígitos: Q001, Q002, etc.)
    colunas_questoes = [col for col in df_unificado.columns if col.startswith('Q')]
    colunas_questoes.sort()  # Ordenar Q001, Q002, Q003, etc.
    
    # Colunas finais
    colunas_finais = colunas_basicas + colunas_questoes
    
    # Selecionar apenas registros que têm nome E resposta
    df_final = df_unificado.dropna(subset=['ID_Nome', 'ID_Resposta'])[colunas_finais].copy()
    
    # Renomear colunas
    df_final = df_final.rename(columns={
        'ID_Nome': 'ID',
        'Nome': 'Nome',
        'Sala': 'Sala',
        'Serie': 'Serie',
        'Respostas_String': 'Gabarito_Completo'
    })
    
    # Preencher valores vazios
    df_final['Sala'] = df_final['Sala'].fillna('Sala_Não_Identificada')
    
    # Gerar timestamp para nomenclatura dos arquivos
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nome_arquivo_excel = f"Resultados_{timestamp}.xlsx"
    
    # Salvar resultados
    print(f"\n💾 SALVANDO ARQUIVO EXCEL:")
    
    # Excel com múltiplas abas
    with pd.ExcelWriter(nome_arquivo_excel, engine='openpyxl') as writer:
        # Aba principal com dados unificados
        df_final.to_excel(writer, sheet_name='Dados_Completos', index=False)
        
        # Aba com alunos SEM cartão de resposta
        df_sem_cartao = df_unificado[df_unificado['ID_Resposta'].isnull()][['ID_Nome', 'Nome', 'Sala']].copy()
        if not df_sem_cartao.empty:
            df_sem_cartao = df_sem_cartao.rename(columns={
                'ID_Nome': 'ID',
                'Nome': 'Nome',
                'Sala': 'Sala'
            })
            df_sem_cartao.to_excel(writer, sheet_name='Alunos_Sem_Cartao', index=False)
            print(f"   - Alunos_Sem_Cartao: {len(df_sem_cartao)} alunos sem cartão")
        
        # Aba com cartões SEM aluno
        df_sem_aluno = df_unificado[df_unificado['ID_Nome'].isnull()][['ID_Resposta', 'Respostas_String']].copy()
        if not df_sem_aluno.empty:
            df_sem_aluno = df_sem_aluno.rename(columns={
                'ID_Resposta': 'ID_Cartao',
                'Respostas_String': 'Respostas'
            })
            df_sem_aluno.to_excel(writer, sheet_name='Cartoes_Sem_Aluno', index=False)
            print(f"   - Cartoes_Sem_Aluno: {len(df_sem_aluno)} cartões sem aluno")
        
        # Aba de estatísticas
        stats_data = {
            'Métrica': [
                'Total de Alunos com Nome',
                'Total de Cartões de Resposta', 
                'Alunos com Nome E Resposta',
                'Nomes sem Cartão',
                'Cartões sem Nome',
                'Taxa de Correspondência (%)',
                'Total de Questões'
            ],
            'Valor': [
                len(df_nomes),
                len(df_respostas),
                total_unificados,
                nomes_sem_resposta,
                respostas_sem_nome,
                round((total_unificados / max(len(df_nomes), len(df_respostas))) * 100, 1),
                len(colunas_questoes)
            ]
        }
        
        df_stats = pd.DataFrame(stats_data)
        df_stats.to_excel(writer, sheet_name='Estatisticas', index=False)
        
        # Abas separadas por série
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
                print(f"   - {nome_aba}: {len(df_serie)} alunos")
        
        # Aba de resumo das salas
        if not df_final.empty:
            df_resumo_salas = df_final.groupby('Sala').agg({
                'ID': 'count'
            }).rename(columns={'ID': 'Quantidade_Alunos'}).reset_index()
            df_resumo_salas.to_excel(writer, sheet_name='Resumo_Salas', index=False)
    
    print(f"✅ Excel salvo: '{nome_arquivo_excel}'")
    print(f"   📋 Abas criadas:")
    print(f"   - Dados_Completos: Todos os dados unificados")
    if not df_unificado[df_unificado['ID_Resposta'].isnull()].empty:
        print(f"   - Alunos_Sem_Cartao: Alunos que não têm cartão de resposta")
    if not df_unificado[df_unificado['ID_Nome'].isnull()].empty:
        print(f"   - Cartoes_Sem_Aluno: Cartões que não têm aluno correspondente") 
    print(f"   - Estatisticas: Resumo geral")
    print(f"   - Resumo_Salas: Quantidade de alunos por sala")
    
    # Preview
    print(f"\n👁️ PREVIEW DOS DADOS FINAIS:")
    print(f"Colunas: {list(df_final.columns)}")
    print(f"\nPrimeiros registros:")
    print(df_final.head())
    
    print(f"\n🎉 PROCESSAMENTO UNIFICADO CONCLUÍDO COM SUCESSO!")
    print(f"📊 {total_unificados} alunos processados com nome e respostas")
    print(f"📝 {len(colunas_questoes)} questões separadas em colunas individuais")
    print(f"📚 Abas criadas por série: 8º Ano, 9º Ano, 1ª Série, 2ª Série")
    print(f"📅 Arquivo Excel salvo com timestamp: {timestamp}")
    print(f"🔍 {len(arquivos_nomes)} arquivos de nomes e {len(arquivos_respostas)} de respostas processados automaticamente")
    
    return nome_arquivo_excel, df_final

if __name__ == "__main__":
    main()