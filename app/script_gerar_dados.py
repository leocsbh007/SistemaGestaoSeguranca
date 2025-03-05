from sqlalchemy.orm import Session
from sqlalchemy import inspect
from faker import Faker
from app.models.base import SessionLocal, engine
from app.models.user import DBUser, DBRole, RoleType
from app.models.resource import DBResource, ResourceType, StatusType
from app.models.loan import DBLoan, LonasStatus
from datetime import datetime, timedelta
from app.auth import security

# Criando sessão do banco de dados
db: Session = SessionLocal()

# Verificando se as tabelas já foram criadas no banco
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

required_tables = {"users", "roles", "resources", "loans"}
if not required_tables.issubset(existing_tables):
    print("O banco de dados não está inicializado corretamente!")
    print("Por favor, execute o sistema pelo menos uma vez antes de rodar este script.")
    exit(1)

# Criando instância do Faker para gerar dados fictícios
fake = Faker()

# Criando usuários
count = 1   # Contador para criar varios Roles para os usuarios
users = []
for i in range(1, 21):
    username = f"user{i}"  # Exemplo: user0, user1, user2
    # username = fake.first_name().lower()
    email = f"{username}@email.com"

    user = DBUser(
        username=username,        
        hashed_password=security.hash_password("1234"),
        email=email,
        is_active=True,
        is_admin=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Criando um papel para o usuário
    if count < 6:        
        role = DBRole(
            role_type=RoleType.FUNCIONARIO,
            user_id=user.id
        )
        user.is_admin=False
    elif count < 11:
        role = DBRole(
            role_type=RoleType.ADMIN,
            user_id=user.id
        )
        user.is_admin=True
    elif count < 16:
        role = DBRole(
            role_type=RoleType.ADMIN_SEGURANCA,
            user_id=user.id
        )    
        user.is_admin=False
    else:        
        role = DBRole(
            role_type=RoleType.GERENTE,
            user_id=user.id
        )
        user.is_admin=False
    count = count + 1
    
    db.add(role)
    users.append(user)
    db.commit()

# Criando recursos
count = 1
resources = []
for i in range(1, 21):
    if count < 8:
        type=ResourceType.EQUIPAMENTO
    elif count < 14:
        type=ResourceType.DISPOSITIVO_SEGURANCA
    else:
        type=ResourceType.VEICULO
    count = count + 1

    resource = DBResource(
        asset_number=f"WAYNE-{i:03d}",
        name=f"Recurso-{i}",
        type=type.value,
        description=f"Descrição do recurso {i}",
        status=StatusType.DISPONIVEL
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    resources.append(resource)

db.commit()

# Criando empréstimos
for i in range(20):
    start_date = datetime.now() - timedelta(days=fake.random_int(min=1, max=30))
    end_date = start_date + timedelta(days=fake.random_int(min=1, max=15))
    loan = DBLoan(
        start_date=start_date,
        end_date=end_date,
        status=LonasStatus.ATIVO,
        user_id=users[i].id,
        resource_id=resources[i].id
    )
    db.add(loan)

db.commit()

print("Dados inseridos com sucesso!")

# Fechando sessão
db.close()
