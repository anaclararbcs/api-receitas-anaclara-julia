from fastapi import FastAPI

app = FastAPI(title='API julia e ana clara')

@app.get("/aluno")
def get_aluno():
    return {"nome do aluno apos /"}

@app.get("/aluno/{nome_aluno}")
def get_aluno_by_name(nome_aluno: str):
    return {"o nome do aluno é": nome_aluno}