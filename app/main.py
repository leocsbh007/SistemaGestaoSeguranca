from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import create_all
from app.models.database import initialize_admin
from app.routes.auth import router as auth_router  # Importando as rotas de autenticação
from app.routes.user import router as user_router  # Importando as rotas de usuários
from contextlib import asynccontextmanager


# Para iniciar a aplicação e criar as tabelas do banco
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all() # Cria as tabelas do Banco
    # UserCreate.model_rebuild()  # Chama o método rebuild()
    yield # Abaixo pode ser inserido um codigo para quando a aplicação para de rodar

app = FastAPI(lifespan=lifespan, title="API Sistema de Gestão de Segurança", version="0.1")
# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permitir apenas o front-end local
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)


#with next(get_db()) as db:
initialize_admin()

# Incluindo as rotas no app Fast API
app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(user_router, prefix="", tags=["User"])

@app.get("/")
def read_root():
    return {"message": "API Funcionando"}