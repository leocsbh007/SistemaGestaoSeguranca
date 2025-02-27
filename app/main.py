from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import create_all
from app.models.database import initialize_admin
from app.routes.auth import router as auth_router  # Importando as rotas de autenticação
from app.routes.user import router as user_router  # Importando as rotas de usuários
from app.routes.resource import router as resource_router  # Importando as rotas de recursos
from contextlib import asynccontextmanager


# Para iniciar a aplicação e criar as tabelas do banco
@asynccontextmanager
async def lifespan(app: FastAPI):

    create_all() # Cria as tabelas do Banco
    
    # Apos criar a tabela verifica se existe um admin cadastrado
    initialize_admin()  

    yield # Abaixo pode ser inserido um codigo para quando a aplicação para de rodar

app = FastAPI(lifespan=lifespan, title="API Sistema de Gestão de Segurança", version="0.1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    erros = {}

    for error in exc.errors():
        campo = error["loc"][-1] # Pega apenas o campo nome
        mensagem = "O campo é obrigatorio" if error["type"] == "value_error.missing" else error["msg"]
        erros[campo] = mensagem
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, 
        content={"detail": "Erros de validação", "fields": erros}
        )


# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permitir apenas o front-end local
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)


# Incluindo as rotas no app Fast API
app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(user_router, prefix="", tags=["User"])
app.include_router(resource_router, prefix="", tags=["Resource"])

@app.get("/")
def read_root():
    return {"message": "API Funcionando"}