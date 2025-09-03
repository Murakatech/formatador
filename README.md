# 🌐 Formatador de Dados Escolares v4.0 - Online

Sistema completo para processamento e formatação de dados escolares **disponível online** através de navegadores web.

## 🎯 **NOVIDADE v4.0: Aplicação Web Online!**

✨ **Agora disponível na internet para acesso de qualquer lugar!**
- 🌐 **Acesso via navegador** - sem instalações
- 📱 **Funciona em celulares** e tablets
- 🔗 **Compartilhamento fácil** via link
- ☁️ **Deploy em nuvem** gratuito
- 🔒 **Seguro e privado** - dados não são armazenados

## 🚀 Funcionalidades

### ✨ Principais Recursos
- **📤 Upload Manual**: Interface para upload direto de arquivos
- **📊 Dashboard Interativo**: Interface web moderna e intuitiva
- **📚 Organização por Série**: Abas separadas para cada série (8º Ano, 9º Ano, 1ª Série, 2ª Série)
- **📅 Nomenclatura com Timestamp**: Arquivos salvos com data e hora
- **🌐 Aplicação Web**: Disponível online via navegador
- **📈 Estatísticas em Tempo Real**: Métricas e gráficos dos dados processados
- **📝 Suporte Expandido**: Processa até 200 questões (Q001-Q200)
- **⭐ Preservação de Asteriscos**: Mantém asteriscos nas posições exatas

### 📋 Formatos Suportados
- **Entrada**: Arquivos .txt com nomes e respostas
- **Saída**: Arquivo Excel (.xlsx) com múltiplas abas

## 🛠️ Como Usar

### 🌐 **Opção 1: Acesso Online (RECOMENDADO)**

**Acesse diretamente pelo navegador - sem instalações:**

1. **🔗 Acesse**: [Link da aplicação online] (será fornecido após deploy)
2. **📁 Upload**: Faça upload dos seus arquivos de nomes e respostas
3. **🚀 Processe**: Clique em processar e aguarde
4. **📥 Baixe**: Download do arquivo Excel processado

**✅ Vantagens:**
- 🌐 Funciona em qualquer dispositivo
- 📱 Acesso via celular/tablet
- 💻 Sem instalação necessária
- 🔄 Sempre atualizado
- 🔒 Seguro e privado

### 🐳 **Opção 2: Deploy Próprio**

**Para hospedar sua própria versão:**

📖 **Consulte**: `DEPLOY_ONLINE.md` para instruções completas

**Opções disponíveis:**
- 🎯 **Streamlit Cloud** (gratuito)
- 🚂 **Railway** (gratuito)
- 🎨 **Render** (gratuito)
- 🐳 **Docker** (qualquer servidor)

### 🔧 **Opção 3: Desenvolvimento Local**

```bash
# 1. Clone o projeto
git clone <repositorio>
cd formatador

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute localmente
streamlit run dashboard.py
```

## 📁 Estrutura de Arquivos

```
formatador/
├── 📄 dashboard.py          # Interface web principal
├── 📄 formatador.py         # Motor de processamento
├── 📄 build_exe.py          # Script para gerar executável
├── 📄 requirements.txt      # Dependências do projeto
├── 📄 README.md            # Este arquivo
└── 📁 nomes e respostas/   # Pasta com arquivos de exemplo
    ├── 📄 nomes_1serie.txt
    ├── 📄 respostas_1serie.txt
    └── ...
```

## 🌐 **Acesso Remoto (NOVO!)**

### 🏠 **Acesso Local**
- **URL**: `http://localhost:8501`
- **Uso**: Apenas no computador que está executando

### 🌍 **Acesso na Rede**
- **URL**: `http://SEU_IP:8501`
- **Como descobrir seu IP**: Abra CMD e digite `ipconfig`
- **Exemplo**: `http://192.168.1.100:8501`
- **Uso**: Outras pessoas na mesma rede podem acessar

### 📱 **Acesso pelo Celular**
- Use o mesmo IP da rede: `http://SEU_IP:8501`
- Funciona em qualquer dispositivo com navegador

## 🎯 Como Usar o Dashboard

### 📤 Upload Manual de Arquivos
1. **📁 Upload**: Faça upload dos seus arquivos de nomes e respostas
2. **🚀 Processar**: Clique em "Processar Arquivos"
3. **📊 Visualizar**: Analise os resultados e estatísticas
4. **📥 Baixar**: Download do arquivo Excel processado

### ✨ Funcionalidades Disponíveis
- **📊 Métricas**: Total de alunos, séries, salas e questões
- **📈 Gráficos**: Distribuição por série
- **👁️ Preview**: Visualização dos primeiros registros
- **⚠️ Alertas**: Identificação de problemas nos dados
- **📝 Suporte**: Até 200 questões com preservação de asteriscos

## 📊 Estrutura do Excel Gerado

### 📋 Abas Criadas
- **Dados_Completos**: Todos os dados unificados
- **8_Ano**: Apenas alunos do 8º ano
- **9_Ano**: Apenas alunos do 9º ano
- **1_Serie**: Apenas alunos da 1ª série
- **2_Serie**: Apenas alunos da 2ª série
- **Estatisticas**: Resumo geral dos dados
- **Resumo_Salas**: Quantidade de alunos por sala

### 📝 Colunas Principais
- **ID**: Código do aluno
- **Nome**: Nome completo
- **Sala**: Sala/turma
- **Serie**: Série/ano escolar
- **Gabarito_Completo**: String com todas as respostas
- **Q001-Q200**: Questões individuais (expandido para 200 questões)
- **⭐ Asteriscos**: Preservados nas posições exatas conforme necessário

## 📦 **Como Distribuir para Outras Pessoas**

### 🎯 **Método Simples (RECOMENDADO)**

1. **📁 Compacte** toda a pasta `FormatadorPortavel` em um arquivo ZIP
2. **📤 Envie** por:
   - 📧 Email (se < 25MB)
   - ☁️ Google Drive / OneDrive
   - 📁 WeTransfer (até 2GB grátis)
   - 💾 Pendrive / HD externo

3. **📋 Instrua** a pessoa:
   - Extrair o ZIP
   - Executar `Instalar_e_Executar.bat`
   - Aguardar a instalação automática
   - Usar normalmente!

### ✅ **Vantagens desta Abordagem**
- ✅ **Zero configuração** para o usuário final
- ✅ **Funciona sem Python** pré-instalado
- ✅ **Instalação automática** de tudo
- ✅ **Acesso remoto** já configurado
- ✅ **Um arquivo só** para distribuir

### 🔧 **Para Desenvolvedores: Gerando Executável**

```bash
# Se quiser criar um executável tradicional
pip install pyinstaller
pyinstaller --onefile dashboard.py
```

**Mas a instalação automática é mais prática!**

## 📋 Padrões de Arquivos

### 📁 Arquivos de Nomes
- **Padrão**: Devem conter "nomes" no nome
- **Exemplos**: `nomes_1serie.txt`, `nomes 8° ano.txt`
- **Formato**: Código do aluno + Nome (separados por tab ou espaço)

### 📝 Arquivos de Respostas
- **Padrão**: Devem conter "respostas" no nome
- **Exemplos**: `respostas_1serie.txt`, `respostas 8° ano.txt`
- **Formato**: N + Código + String de respostas (A, B, C, D, E, *)

## 🎨 Interface do Dashboard

### 🎛️ Painel de Controle
- **Modo de Operação**: Automático ou Manual
- **Upload de Arquivos**: Drag & drop ou seleção
- **Processamento**: Botão único para executar

### 📊 Visualização de Resultados
- **Métricas**: Total de alunos, séries, salas, questões
- **Gráficos**: Distribuição por série
- **Preview**: Primeiras linhas dos dados
- **Download**: Botão para baixar Excel

## ⚠️ Requisitos do Sistema

### 💻 Para Executável
- **SO**: Windows 7 ou superior
- **RAM**: 2GB mínimo
- **Espaço**: 500MB livres
- **Navegador**: Qualquer navegador moderno

### 🐍 Para Instalação Python
- **Python**: 3.8 ou superior
- **Dependências**: Listadas em `requirements.txt`

## 🆘 Solução de Problemas

### ❌ Arquivos não encontrados
- Verifique se os nomes contêm "nomes" e "respostas"
- Certifique-se de que estão na pasta correta
- Verifique a codificação dos arquivos (UTF-8)

### 🐛 Erro no processamento
- Verifique o formato dos dados nos arquivos
- Certifique-se de que os códigos dos alunos estão corretos
- Verifique se há caracteres especiais

### 🌐 Dashboard não abre
- Verifique se a porta 8501 está livre
- Tente acessar manualmente: `http://localhost:8501`
- Reinicie o programa

## 📞 Suporte

### 🔍 Logs e Debug
- O dashboard mostra mensagens de erro em tempo real
- Verifique o terminal para logs detalhados
- Use o modo manual para upload direto

### 📧 Contato
- Para problemas técnicos, verifique os logs
- Para dúvidas sobre formato de dados, consulte os exemplos
- Para melhorias, sugira novas funcionalidades

## 🎉 Changelog

### v3.0 - Dashboard Interativo
- ✅ Interface web com Streamlit
- ✅ Upload manual de arquivos
- ✅ Executável standalone
- ✅ Remoção da pasta dados_por_sala

### v2.0 - Detecção Automática
- ✅ Busca recursiva de arquivos
- ✅ Processamento de múltiplas séries
- ✅ Nomenclatura com timestamp
- ✅ Abas separadas por série

### v1.0 - Versão Original
- ✅ Processamento básico
- ✅ Geração de Excel
- ✅ Separação por salas

---

**📊 Formatador de Dados Escolares** - Desenvolvido para facilitar o processamento de dados educacionais com máxima eficiência e usabilidade.

*Desenvolvido por Caio Murakami*