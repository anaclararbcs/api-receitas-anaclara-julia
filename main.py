from http import HTTPStatus
from fastapi import FastAPI, HTTPException  
from typing import List
from schema import CreateReceita, Receita, Usuario, BaseUsuario, UsuarioPublic

app = FastAPI(title='API da Ana Clara e da Júlia Emily')

usuarios: List[Usuario] = []

receitas: List[Receita] = []

def receita_existe(nome: str):
    for receita in receitas:
        if receita.nome == nome:
            return True
    return False


def receita_por_id(id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    return None

def receita_por_nome(nome: str):
    for receita in receitas:
        if receita.nome == nome:
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
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")

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
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Campos obrigatórios não podem estar vazios")

    for r in receitas:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")

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


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuarios(dados: BaseUsuario):
    if not usuarios:
        novo_id = 1
    else:
        novo_id = usuarios[-1].id + 1

    for u in usuarios:
        if u.email.lower() == dados.email.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário com esse email")

    novo_usuario = UsuarioPublic(
        id=novo_id,
        nome_usuario=dados.nome_usuario,
        email=dados.email,
    )

    usuarios.append(novo_usuario)

    return novo_usuario

from http import HTTPStatus
from fastapi import FastAPI, HTTPException  
from typing import List
from schema import CreateReceita, Receita, Usuario, BaseUsuario, UsuarioPublic

app = FastAPI(title='API da Ana Clara e da Júlia Emily')

usuarios: List[Usuario] = []

receitas: List[Receita] = []

def Usuario_existe(nome: str):
    for usuario in usuarios:
        if usuario.nome == nome:
            return True
    return False


def usuario_por_id(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    return None

def usuario_por_nome(nome: str):
    for usuario in usuarios:
        if usuario.nome == nome:
            return usuario
    return None

@app.get("/", status_code=HTTPStatus.OK)
def hello():
    return {"title": "Livro de Usuarios"}

@app.get("/usuarios", response_model=List[Usuario], status_code=HTTPStatus.OK)
def get_todos_usuarios():
    return usuarios


@app.get("/usuarios/id/{id}", response_model=Usuario, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")


@app.get("/usuarios/{nome_usuario}", response_model=Usuario, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str):
    for usuario in usuarios:
        if usuario.nome.lower() == nome_usuario.lower():
            return usuario
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")


@app.post("/usuarios", response_model=Usuario, status_code=HTTPStatus.CREATED)
def create_Usuario(dados: create_usuarios):
    if not usuarios:
        novo_id = 1
    else:
        novo_id = usuarios[-1].id + 1

    for r in usuarios:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuario com esse nome")

    novo_usuario = Usuario(
        id=novo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )
    receitas.append(novo_usuario)
    return novo_usuario


@app.put("/usuarios/{id}", response_model=Usuario, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: create_usuarios):
    if not dados.nome or not dados.modo_de_preparo or not dados.ingredientes:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Campos obrigatórios não podem estar vazios")

    for r in usuarios:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuario com esse nome")

    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_atualizado = Usuario(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo
            )
            usuarios[i] = usuario_atualizado
            return usuario_atualizado

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")


@app.delete("/usuarios/{id}", response_model=Usuario, status_code=HTTPStatus.OK)
def deletar_usuario(id: int):
    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_deletado = usuarios.pop(i)
            return usuario_deletado 

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")