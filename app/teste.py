from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User  # Supondo que você tenha um modelo User já definido

# Crie o engine e a sessão
engine = create_engine('sqlite:///meu_banco.db')
Session = sessionmaker(bind=engine)
session = Session()

# Use o ORM para fazer a consulta
users = session.query(User).all()

# Exiba os resultados
for user in users:
    print(user)