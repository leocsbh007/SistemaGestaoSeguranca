from fastapi import FastAPI
# from app.routes import auth, user
from app.schemas.user import UserCreate  # Importe o UserCreate aqui
from app.routes.auth import router as auth_router  # Importando as rotas de autenticação
from app.routes.user import router as user_router  # Importando as rotas de usuários

from app.models.base import create_all
from contextlib import asynccontextmanager


# Para iniciar a aplicação e criar as tabelas do banco
@asynccontextmanager
async def lifespan(app: FastAPI):

    create_all() # Cria as tabelas do Banco
    # UserCreate.model_rebuild()  # Chama o método rebuild()
    yield # Abaixo pode ser inserido um codigo para quando a aplicação para de rodar

app = FastAPI(lifespan=lifespan, debug=True)

# Incluindo as rotas no app Fast API
# app.include_router(auth.router, prefix="/auth", tags=["authentication"])
# app.include_router(user.router, prefix="/user", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])

@app.get("/")
def read_root():
    return {"message": "API Funcionando"}