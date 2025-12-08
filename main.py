from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from schema import CreateReceita, Receita, BaseUsuario, UsuarioPublic
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_session
from sqlalchemy.exc import IntegrityError

receitas: List[Receita] = []

app = FastAPI(title="API de Receitas")


def receita_existe(nome: str):
    return any(receita.nome.lower() == nome.lower() for receita in receitas)


def receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    return None


@app.get("/", status_code=HTTPStatus.OK)
def hello():
    return {"title": "Livro de Receitas"}


@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas


@app.get("/receitas/id/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_id(id: int):
    receita = receita_por_id(id)
    if not receita:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")
    return receita


@app.get("/receitas/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: CreateReceita):
    if receita_existe(dados.nome):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")

    novo_id = 1 if not receitas else receitas[-1].id + 1

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
    receita = receita_por_id(id)
    if not receita:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

    for r in receitas:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")

    receita.nome = dados.nome
    receita.ingredientes = dados.ingredientes
    receita.modo_de_preparo = dados.modo_de_preparo

    return receita


@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            return receitas.pop(i)
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/usuarios", response_model=UsuarioPublic, status_code=HTTPStatus.CREATED)
def create_usuario(dados: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.nome_usuario == dados.nome_usuario) |
            (User.email == dados.email)
        )
    )

    if db_user:
        if db_user.nome_usuario == dados.nome_usuario:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Nome de usuário já existe",
            )
        if db_user.email == dados.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email já existe",
            )

    db_user = User(
        nome_usuario=dados.nome_usuario,
        senha=dados.senha,
        email=dados.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    usuarios = session.scalars(select(User).offset(skip).limit(limit)).all()
    return usuarios


@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    return db_user


@app.get("/usuarios/nome/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.nome_usuario == nome_usuario))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    return db_user


@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    try:
        db_user.nome_usuario = dados.nome_usuario
        db_user.senha = dados.senha
        db_user.email = dados.email

        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Nome de usuário ou email já existe"
        )


@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def deletar_usuario(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    session.delete(db_user)
    session.commit()

    return db_user
