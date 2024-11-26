from openai import OpenAI
from groq import Groq

class LLM:
    def __init__(self, api_key, modelo, temperatura=0.5, quantidade_tokens=150, mensagem=""):
        self.temperatura = temperatura
        self.quantidade_tokens = quantidade_tokens
        self.mensagem = mensagem
        self.modelo = modelo
        self.api_key = api_key
        self.openai_client = None
        self.groq_client = None

    def _init_openai_client(self):
        if not self.openai_client:
            self.openai_client = OpenAI(api_key=self.api_key)

    def _init_groq_client(self):
        if not self.groq_client:
            self.groq_client = Groq(api_key=self.api_key)

    def gerar_resposta_openai(self):
        self._init_openai_client()
        messages = []
        
        if self.mensagem.strip():
            messages.append({"role": "system", "content": self.mensagem})
        
        messages.append({"role": "user", "content": self.prompt})
        
        response = self.openai_client.chat.completions.create(
            model=self.modelo,
            messages=messages,
            temperature=self.temperatura,
            max_tokens=self.quantidade_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()

    def gerar_resposta_groq(self):
        self._init_groq_client()
        messages = []
        
        if self.mensagem.strip():
            messages.append({"role": "system", "content": self.mensagem})
        
        messages.append({"role": "user", "content": self.prompt})
        
        completion = self.groq_client.chat.completions.create(
            model=self.modelo,
            messages=messages,
            temperature=self.temperatura,
            max_tokens=self.quantidade_tokens,
            top_p=0.65,
            stream=False,  # Mudamos para False para manter consistência com OpenAI
            stop=None
        )
        return completion.choices[0].message.content.strip()

    def gerar_resposta(self):
        """Método principal para gerar respostas baseado no modelo selecionado"""
        if "gpt" in self.modelo:  # Modelos OpenAI
            return self.gerar_resposta_openai()
        elif "llama" in self.modelo or "mixtral" in self.modelo:  # Modelos Groq
            return self.gerar_resposta_groq()
        else:
            raise ValueError(f"Modelo não suportado: {self.modelo}")


