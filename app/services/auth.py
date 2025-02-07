from passlib.context import CryptContext

# Cria um contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Função para hash de senha
def hash_password(password: str):
    return pwd_context.hash(password)

# Função para verificar a Senha
def verify_password(entered_password, hashed_password):
    # print(f"Senha digitada: {entered_password}")
    # print(f"Senha hash armazenada {hashed_password}")
    return pwd_context.verify(entered_password, hashed_password)