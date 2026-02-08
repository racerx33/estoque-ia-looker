import streamlit as st
import ai_engine
import db_manager
import response_engine
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configuração da Página - Modo "Wide" ajuda na visualização em iframes
st.set_page_config(page_title="IA Chat", layout="wide")

# CSS para remover o padding superior e deixar o chat mais "colado" no topo
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inicializar histórico de chat na sessão do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto (Chat Input)
if prompt := st.chat_input("Pergunte sobre os dados deste dashboard..."):
    # 1. Mostrar pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Processamento (Camadas Modulares)
    with st.chat_message("assistant"):
        # O spinner dá o feedback visual de que a IA está trabalhando
        with st.spinner("Analisando dados..."):
            try:
                # Fase 1: Geração do SQL
                query = ai_engine.gerar_query_sql(prompt)
                
                # Fase 2: Busca no MySQL
                dados = db_manager.executar_consulta(query)
                
                # Fase 3: Resposta em Linguagem Natural
                resposta = response_engine.gerar_resposta_final(prompt, dados)
                
                # Exibição da resposta
                st.markdown(resposta)
                
                # Salva no histórico
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                
            except Exception as e:
                st.error("Houve um problema ao processar sua consulta.")