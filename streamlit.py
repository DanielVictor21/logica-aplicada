import os
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
import streamlit as st

load_dotenv()
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    st.error("API_KEY não foi carregada. Verifique se o arquivo .env está configurado corretamente.")
else:
    def llm_call(question):
        client = OpenAI(api_key=API_KEY)
        prompt = """
            Você precisará analisar uma frase, dividida entre hipótese e tese. /
            Depois, você precisará classficar o argumento em quatro tipos: Dedutivo válido, Dedutivo inválido, Indutivo Fraco e Indutivo forte. /
            Exemplos:
            Dedutivo Válido = 'Baleia é mamífero; Mamífero não é peixe. Logo a baleia não é peixe.' /
            Dedutivo Inválido = 'Os baianos gostam de carnaval; Eu gosto de carnaval. Logo eu sou baiana.' /
            Indutivo Forte = 'Se fiz o teste da vacina com ratos e funcionou; fiz o mesmo teste com macacos e funcionou; fiz com outros mamíferos e também funcionou, Então a vacina deve funcionar com seres humanos.'/
            Indutivo Fraco = 'Se ontem fui pescar no rio e peguei uma sardinha; hoje fui novamente e pesquei mais sardinhas; Então nesse rio só tem sardinhas.' /
            Logo, analise a SINTAXE e a SEMÂNTICA de cada frase, e sua resposta será um desses tipos de argumentos.
            """
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.3,
            seed=42,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ]
        )
        response = response.choices[0].message.content
        
        return response

    st.title("Classificação de Argumentos Lógicos")
    question = st.text_area("Digite a frase que deseja analisar:")

    if st.button("Classificar Argumento"):
        if question:
            try:
                response = llm_call(question)
                st.success(f"Resultado da Análise: {response}")
            except Exception as e:
                st.error(f"Ocorreu um erro na análise: {e}")
        else:
            st.warning("Por favor, insira uma frase para análise.")

