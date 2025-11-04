from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title='API da Ana Clara e da Júlia Emily')

class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str


receitas: List[Receita] = []

@app.get("/")
def hello():
    return {"title": "livro de receitas"}

@app.get("/receitas")
def get_todas_receitas():
    return receitas 

@app.get("/receitas/id/{id}")
def get_receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
        return {"mensagem": "receita não encontrada"}
    
@app.get("/receitas/{nome_receita}")
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome == nome_receita:
          return receita
        return {"mensagem": "receita não encontrada"}

@app.post("/receitas")
def create_receita(dados: Receita):
    if not receitas:
        novo_id=1
    else: 
        novo_id = receitas[-1].id+1
        
    nova_receita = Receita(
        id=novo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )
    receitas.append(nova_receita)
    return nova_receita
    
@app.put("/receitas/{id}")
def update_receita(id: int, dados: CreateReceita):
    for r in receitas:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            return {"mensagem": "Já existe uma receita com esse nome"}

    if dados.nome == "" or dados.modo_de_preparo == "" or dados.ingredientes == []:
        return {"mensagem": "Nenhum campo pode estar vazio"}

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo
            )
            receitas[i] = receita_atualizada
            return {"mensagem": "Receita atualizada", "receita": receita_atualizada}
        
    return {"mensagem": "Receita não encontrada"}

@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_deletada = receitas.pop(i)
            return {"mensagem": "Receita deletada"}
        
        return {"mensagem": "Receita não encontrada"}