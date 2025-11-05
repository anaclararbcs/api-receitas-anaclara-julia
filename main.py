from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from typing import List
from .schema import CreateReceita, Receita

app = FastAPI(title='API da Ana Clara e da Júlia Emily')

receitas: List[Receita] = []


@app.get("/", status_code=HTTPStatus.OK)
def hello():
    return {"title": "Livro de Receitas"}

@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas


@app.get("/receitas/id/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.get("/receitas/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: CreateReceita):
    if not receitas:
        novo_id = 1
    else:
        novo_id = receitas[-1].id + 1

    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe uma receita com esse nome"
            )

    nova_receita = Receita(
        id=novo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )
    receitas.append(nova_receita)
    return nova_receita


@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    if not dados.nome or not dados.modo_de_preparo or not dados.ingredientes:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Campos obrigatórios não podem estar vazios"
        )

    for r in receitas:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe uma receita com esse nome"
            )

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo
            )
            receitas[i] = receita_atualizada
            return receita_atualizada

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_deletada = receitas.pop(i)
            return receita_deletada

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")
