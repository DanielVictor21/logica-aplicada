from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
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
        Depois, você precisará classficar o argumento em dois tipos: 1- Dedutivo válido, 2- Dedutivo inválido. O primeiro caractere da sua resposta deve ser o código referente ao tipo. /
        Exemplos:
        Dedutivo Válido = 'Baleia é mamífero; Mamífero não é peixe. Logo a baleia não é peixe.' /
        Dedutivo Inválido = 'Os baianos gostam de carnaval; Eu gosto de carnaval. Logo eu sou baiana.' /
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
    arg_type_mapping = {
         '1': 'Dedutivo válido',
         '2': 'Dedutivo inválido'
    }
    arg_type = arg_type_mapping[response_content[0]]
    
    return arg_type, response_content

# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/", response_class=HTMLResponse)
# async def read_home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send", response_class=HTMLResponse)
async def receive_form(request: Request, prompt: str = Form(...)):
        response, arg_type = llm_call(prompt)
        return JSONResponse(content={"response": response, "arg_type": arg_type})
        # return templates.TemplateResponse("index.html", {"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
