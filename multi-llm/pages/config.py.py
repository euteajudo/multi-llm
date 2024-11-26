import streamlit as st

st.title("Configurações")

# Inicializa o estado da sessão para a mensagem do sistema se não existir
if 'mensagem_sistema' not in st.session_state:
    st.session_state.mensagem_sistema = ""

# Campo de entrada para a mensagem do sistema
mensagem = st.text_area("Mensagem para o sistema:", value=st.session_state.mensagem_sistema, height=150, max_chars=800)

# Botão "OK" para atualizar a mensagem do sistema
if st.button("OK"):
    # Atualiza a mensagem do sistema no estado da sessão
    st.session_state.mensagem_sistema = mensagem

# Exibe a contagem de caracteres
st.write(f"Contagem de caracteres: {len(st.session_state.mensagem_sistema)} / 800")
