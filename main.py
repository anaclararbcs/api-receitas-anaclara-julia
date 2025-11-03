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

'''receitas = [
    {
        "nome": "brownie",
        "ingredientes": ["3 ovos", "6 colheres de açúcar", "2 xícaras de chocolate em pó"],
        "utensilios": ["tigela", "forma"],
        "modo_de_preparo": "Misture tudo e leve ao forno por 40 minutos."
    },
    {
        "nome": "torta",
        "ingredientes": ["3 ovos", "1 xícara de leite", "2 xícaras de farinha"],
        "utensilios": ["liquidificador", "forma"],
        "modo_de_preparo": "Bata tudo no liquidificador e asse por 30 minutos."
    },
    {
        "id"=3,
        "nome": "bolo de cenoura",
        "ingredientes": ["3 cenouras", "3 ovos", "2 xícaras de açúcar"],
        "utensilios": ["liquidificador", "forma"],
        "modo_de_preparo": "Bata os ingredientes e asse por 40 minutos."
    },
]
  [
 {
        "id"=4,
        "nome": "panqueca",
        "ingredientes": ["2 ovos", "1 xícara de leite", "1 xícara de farinha"],
        "utensilios": ["frigideira"],
        "modo_de_preparo": "Bata tudo, despeje na frigideira e recheie a gosto."
    },
    {
        "id"=5,
        "nome": "pudim",
        "ingredientes": ["1 lata de leite condensado", "2 latas de leite", "3 ovos"],
        "utensilios": ["liquidificador", "forma de pudim"],
        "modo_de_preparo": "Bata, caramelize a forma e cozinhe em banho-maria."
    },
    {
        "id"=6,
        "nome": "mousse de maracujá",
        "ingredientes": ["1 lata de leite condensado", "1 lata de creme de leite", "suco de maracujá"],
        "utensilios": ["liquidificador"],
        "modo_de_preparo": "Bata tudo no liquidificador e leve à geladeira."
    }
]
  
]'''

@app.get("/")
def hello():
    return {"title": "Livro de Receitas"}


@app.get("/receitas")
def get_todas_receitas():
    return receitas


@app.get("/receitas/id/{id}")
def get_receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    return {"mensagem": "Receita não encontrada"}


@app.get("/receitas/{nome_receita}")
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    return {"mensagem": "Receita não encontrada"}


@app.post("/receitas")
def create_receita(dados: CreateReceita):
    # Gera ID automaticamente
    novo_id = receitas[-1].id + 1 if receitas else 1

    nova_receita = Receita(
        id=novo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    return {"mensagem": "Receita criada com sucesso!", "receita": nova_receita}


@app.put("/receitas/{id}")
def update_receita(id: int, dados: CreateReceita):
    for r in receitas:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            return {"mensagem": "Já existe uma receita com esse nome"}

    if not dados.nome.strip() or not dados.modo_de_preparo.strip() or not dados.ingredientes:
        return {"mensagem": "Nenhum campo pode estar vazio"}

    for i, receita in enumerate(receitas):
        if receita.id == id:
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo
            )
            receitas[i] = receita_atualizada
            return {"mensagem": "Receita atualizada com sucesso!", "receita": receita_atualizada}

    return {"mensagem": "Receita não encontrada"}


@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    for i, receita in enumerate(receitas):
        if receita.id == id:
            receita_removida = receitas.pop(i)
            return {"mensagem": "Receita deletada com sucesso!", "receita": receita_removida}
    return {"mensagem": "Receita não encontrada"}
