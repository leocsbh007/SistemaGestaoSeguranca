# API Sistema de Gestão de Segurança - BackEnd

## Descrição

Este é um sistema de gestão de segurança desenvolvido com FastAPI, projetado para gerenciar usuários, recursos (equipamentos, veículos, etc.) e empréstimos. A API oferece autenticação baseada em JWT, autorização baseada em roles (ADMIN, FUNCIONARIO, GERENTE, ADMIN_SEGURANCA) e endpoints para operações CRUD em usuários, recursos e empréstimos. 
Foi desenvolvido para atender as epecificações da Infinity School.
* **Infelizmente não consegui fazer a parte da Dashboard até a data de entrega 06/03/2025.**
* **Todo o projeto foi feito usando as praticas de criação de branches e pull requets do git, para ter uma evolução consciente da aplicação, tive mais dificulades no inicio, pois ainda não estava entendendo tão bem o FastAPI, demorei muito na criação da autenticação de nas implementação de usuarios, quando consegui fechar as outras tabelas foi mais facil fazer, pois seguiam a mesma filosofia de implementação.**

## Funcionalidades

*   **Autenticação:** Login com JWT (JSON Web Tokens) para autenticação segura.
*   **Autorização:** Controle de acesso baseado em roles (RBAC) para restringir o acesso a determinados endpoints.
*   **Gerenciamento de Usuários:**
    *   Criar, ler, atualizar e deletar usuários.
    *   Atribuição de roles (ADMIN, FUNCIONARIO, GERENTE, ADMIN_SEGURANCA).
*   **Gerenciamento de Recursos:**
    *   Criar, ler, atualizar e deletar recursos (equipamentos, veículos, etc.).
    *   Atribuição de status (DISPONIVEL, EM_USO, MANUTENCAO).
*   **Gerenciamento de Empréstimos:**
    *   Registrar empréstimos de recursos para usuários.
    *   Controlar o status dos empréstimos (ATIVO, FINALIZADO, ATRASADO).
    *   Definir datas de início e fim dos empréstimos.

## Tecnologias Utilizadas

*   [FastAPI](https://fastapi.tiangolo.com/): Framework web Python moderno e de alto desempenho.
*   [SQLAlchemy](https://www.sqlalchemy.org/): Toolkit SQL e ORM (Object-Relational Mapper) para interagir com o banco de dados.
*   [SQLite](https://www.sqlite.org/): Banco de dados leve e fácil de usar (pode ser substituído por outros bancos de dados).
*   [PyJWT](https://pyjwt.readthedocs.io/): Biblioteca Python para trabalhar com JWTs.
*   [Passlib](https://passlib.readthedocs.io/): Biblioteca para hashing de senhas de forma segura.
*   [Alembic](https://alembic.sqlalchemy.org/en/latest/): Ferramenta para migrações de banco de dados.
*   [uvicorn](https://www.uvicorn.org/): Servidor ASGI para executar a aplicação FastAPI.

## Requisitos

*   Python 3.10.11

## Configuração

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/leocsbh007/SistemaGestaoSeguranca.git
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python3 -m venv venv  # ou python -m venv venv no Windows
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar o Banco de Dados:**

    Por padrão, o sistema usa um banco de dados SQLite (`security.db`). A URL do banco de dados está configurada no arquivo `app/config.py`.  Se você deseja usar outro banco de dados, altere a `DATABASE_URL` no arquivo `app/config.py` e instale o driver apropriado (ex: `psycopg2` para PostgreSQL).
    A aplicação precisa rodar pelo menos uma vez para criar o banco, na criação do banco também é criado um usuario
    - Usuario: Admin
    - Email: admin@email.com
    - Senha: admin1234


## Executando a Aplicação

```bash
uvicorn app.main:app --port 8080 --reload
```

* por algum motivo a porta 8000 parou de funcionar **

# Iniciando o Servidor Uvicorn

Isso iniciará o servidor Uvicorn no modo de desenvolvimento, com recarregamento automático sempre que você fizer alterações no código. A aplicação estará disponível em [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Endpoints da API

A documentação da API pode ser acessada em [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs) após a execução da aplicação. O FastAPI gera automaticamente a documentação Swagger UI.

### Exemplos de Endpoints:

- **POST /auth/login**: Autentica um usuário e retorna um token JWT.
- **GET /users/**: Retorna a lista de usuários (requer autenticação).
- **POST /users/**: Cria um novo usuário (requer autenticação de ADMIN).
- **GET /resources/**: Retorna a lista de recursos (requer autenticação).
- **POST /resources/**: Cria um novo recurso (requer autenticação de ADMIN).
- **POST /loans/**: Cria um novo empréstimo (requer autenticação de ADMIN).

## Autenticação e Autorização

### Autenticação

Para acessar endpoints protegidos, é necessário obter um token JWT através do endpoint `/auth/login` e incluí-lo no cabeçalho **Authorization** das requisições como `Bearer <token>`.

### Autorização

Alguns endpoints exigem que o usuário autenticado tenha uma role específica (ex: ADMIN). O sistema verifica a role do usuário a partir do token JWT.

## Como testar
Utilize um cliente API: Ferramentas como Postman ou Insomnia podem ser usadas para testar a API de forma mais completa.

## Seed de Dados
O projeto inclui um script (app/script_gerar_dados.py) para gerar dados fictícios no banco de dados. Este script cria usuários, recursos e empréstimos para facilitar o teste da aplicação.

Para executar o script:

py -m app.script_gerar_dados # no Windows

# Logging

O projeto utiliza a biblioteca `logging` para registrar eventos importantes. As configurações de logging podem ser encontradas nos arquivos `app/models/base.py`, `app/auth/middleware.py` e outros arquivos de serviço/repositório.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Notas Adicionais

- O arquivo `requirements.txt` lista todas as dependências do projeto.
- O arquivo `app/config.py` contém configurações importantes, como a chave secreta para JWT e a URL do banco de dados.
- O diretório `app/models` contém as definições dos modelos do banco de dados.
- O diretório `app/schemas` contém os esquemas Pydantic para validação de dados.
- O diretório `app/routes` contém as definições das rotas da API.
- O diretório `app/auth` contém a lógica de autenticação e segurança.
- O diretório `app/repositories` contém a lógica para acesso ao banco de dados.
- O arquivo `app/main.py` é o ponto de entrada da aplicação.



