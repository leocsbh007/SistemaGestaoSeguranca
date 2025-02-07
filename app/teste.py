from app.services.auth import verify_password

senha_digitada = "senha123"
senha_armazenada = "$2b$12$X...hash_do_banco..."

print(verify_password(senha_digitada, senha_armazenada))
