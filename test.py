from fastapi import FastAPI 

from sqlalchemy import create_engine 
from sqlalchemy.orm import Session   
from models import User, table_registry

app = FastAPI(title=' API de teste')

engine = create_engine("sqlite:///:memory:", echo=False)

table_registry.metadata.create_all(engine)

with Session(engine) as session: 
    juliana = User(
        nome_usuario="juliana", senha="senha123", email="juliana@gmail.com"
    )
    session.add(juliana)
    session.commit()
    session.refresh(juliana)

print ("DADOS DE USUÁRIO:", juliana)
print ("ID:", juliana.id)
print ("Criado em:", juliana.created_at)