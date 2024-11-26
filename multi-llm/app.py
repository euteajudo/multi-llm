import streamlit as st
from llms import LLM

st.set_page_config(page_title="Multi-LLM", layout="wide", page_icon=":robot_face:", initial_sidebar_state="expanded")
st.title("Multi-LLM 🤖")

st.sidebar.title("Escolha um provedor de LLM")
provider = st.sidebar.selectbox("Provedor", ["OpenAI", "Groq"], key="provider_selectbox")

# Inicializa o estado da sessão se não existir
if 'provider' not in st.session_state:
    st.session_state.provider = provider
    st.session_state.model = None

# Inicializa as chaves API para cada provedor se não existirem
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        "OpenAI": "",
        "Groq": ""
    }

# Campo para API key específica do provedor selecionado
api_key = st.sidebar.text_input(
    f"Insira sua chave API para {provider}:",
    type="password",
    value=st.session_state.api_keys[provider]
)

# Armazena a chave API do provedor atual
if api_key:
    st.session_state.api_keys[provider] = api_key

# Verifica se houve mudança de provedor
if st.session_state.provider != provider:
    st.session_state.provider = provider
    st.session_state.model = None
    st.rerun()

# Adiciona botão para limpar sessão no sidebar
if st.sidebar.button("Novo Chat"):
    # Guarda temporariamente as chaves API e a mensagem do sistema
    api_keys_temp = st.session_state.api_keys
    mensagem_sistema_temp = st.session_state.mensagem_sistema
    provider_temp = st.session_state.provider
    
    # Limpa todo o estado da sessão
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Restaura as chaves API e a mensagem do sistema
    st.session_state.api_keys = api_keys_temp
    st.session_state.mensagem_sistema = mensagem_sistema_temp
    st.session_state.provider = provider_temp
    
    # Força o recarregamento da página
    st.rerun()

# Só mostra o select de modelos se tiver API key para o provedor atual
if st.session_state.api_keys[provider]:
    # Define os modelos disponíveis para cada provedor
    models = {
        "OpenAI": ["gpt-4", "gpt-4o-mini", "gpt-3.5-turbo"],
        "Groq": [
            "llama3-groq-70b-8192-tool-use-preview",
            "llama-3.1-70b-versatile",
            "llama-3.2-90b-vision-preview"
        ]
    }
    
    # Inicializa as configurações no estado da sessão se não existirem
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = models[provider][0]  # Primeiro modelo como padrão
    
    if 'temperatura' not in st.session_state:
        st.session_state.temperatura = 0.5  # Valor padrão
    
    if 'quantidade_tokens' not in st.session_state:
        st.session_state.quantidade_tokens = 150  # Valor padrão
    
    if 'quantidade_tokens_input' not in st.session_state:
        st.session_state.quantidade_tokens_input = ""  # Valor padrão
    
    # Mostra selectbox com os modelos do provedor escolhido e atualiza o estado da sessão
    selected_model = st.sidebar.selectbox(
        "Escolha o modelo:",
        models[provider],
        key="model_selectbox",
        index=models[provider].index(st.session_state.selected_model) if st.session_state.selected_model in models[provider] else 0
    )
    st.session_state.selected_model = selected_model
    
    # Controles para temperatura
    temperatura = st.sidebar.slider(
        "Temperatura:",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperatura,
        step=0.1
    )
    st.session_state.temperatura = temperatura

    # Campo para quantidade de tokens (opcional)
    quantidade_tokens_input = st.sidebar.text_input(
        "Quantidade de tokens (deixe em branco para padrão):",
        value=st.session_state.quantidade_tokens_input,
        placeholder="Ex: 150"
    )
    st.session_state.quantidade_tokens_input = quantidade_tokens_input

    # Converte a entrada para um número ou usa o padrão
    if quantidade_tokens_input.strip() == "":  # Se o campo estiver vazio
        quantidade_tokens = 150  # Valor padrão
    else:
        quantidade_tokens = int(quantidade_tokens_input) if quantidade_tokens_input.isdigit() else 150  # Converte ou usa padrão
    
    st.session_state.quantidade_tokens = quantidade_tokens

    # Verifica se a mensagem do sistema foi inicializada
    if 'mensagem_sistema' not in st.session_state:
        st.session_state.mensagem_sistema = ""  # Inicializa se não existir

    # Recupera a mensagem do sistema do estado da sessão
    mensagem = st.session_state.mensagem_sistema

    # Cria o container para o chat
    chat_container = st.container()
    
    # Inicializa o histórico de mensagens se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra histórico de mensagens
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Campo de entrada do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adiciona mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostra mensagem do usuário
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            
            # Placeholder para resposta do assistente
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.write("Pensando...")
                
                # Chama a função para gerar a resposta com base no provedor selecionado
                llm_instance = LLM(
                    api_key=st.session_state.api_keys[provider],
                    modelo=st.session_state.selected_model,
                    temperatura=st.session_state.temperatura,
                    quantidade_tokens=st.session_state.quantidade_tokens,
                    mensagem=st.session_state.mensagem_sistema
                )
                llm_instance.prompt = prompt
                response = llm_instance.gerar_resposta()
                message_placeholder.write(response)
        
        # Adiciona resposta do assistente ao histórico        
        st.session_state.messages.append({"role": "assistant", "content": response})
