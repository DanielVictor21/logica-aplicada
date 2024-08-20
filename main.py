from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
app = FastAPI()

def llm_call(question):
    client = OpenAI(api_key=API_KEY)
    prompt = """
        Você precisará analisar uma frase, dividida entre hipótese e tese. /
        Depois, você precisará classficar o argumento em quatro tipos: Dedutivo válido, Dedutivo inválido, Indutivo Fraco e Indutivo forte. /
        Exemplos:
        Dedutivo Válido = 'Baleia é mamífero; Mamífero não é peixe. Logo a baleia não é peixe.' /
        Dedutivo Inválido = 'Os baianos gostam de carnaval; Eu gosto de carnaval. Logo eu sou baiana.' /
        Indutivo Forte = 'Se fiz o teste da vacina com ratos e funcionou; fiz o mesmo teste com macacos e funcionou; fiz com outros mamíferos e também funcionou, Então a vacina deve funcionar com seres humanos.'/
        Indutivo Fraco = 'Se ontem fui pescar no rio e peguei uma sardinha; hoje fui novamene e pesquei mais sardinhas; Então nesse rio só tem sardinhas.' /
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
    response_content = response.choices[0].message.content
    
    return response_content

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send", response_class=HTMLResponse)
async def receive_form(request: Request, prompt: str = Form(...)):
        response = llm_call(prompt)
        return templates.TemplateResponse("index.html", {"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
