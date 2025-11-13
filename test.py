from fastapi import FastAPI 

from sqlalchemy import create_engine 
from sqlalchemy.orm import Session  
from models import User, table_registry

app = FastAPI(title=' API de teste')

engine = create_engine("sqlite:///:memory:", echo=False)

table_registry.metadata.create_all(engine)

with Session(engine) as session: 
    mairon = User(
        username="mairon", password="senha123", email="mairon@gmail.com"
    )
    session.add(mairon)
    session.commit()
    session.refresh(mairon)

print ("DADOS DE USUÁRIO:", mairon)
print ("ID:", mairon.id)
print ("Criado em:", mairon.created_at)