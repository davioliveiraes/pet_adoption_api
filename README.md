# Pet Adoption API

API RESTful para gerenciamento de adoção de animais de estimação, desenvolvida com **Python** e **Flask**, seguindo os princípios de **Clean Architecture** e padrão **MVC**.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Banco de Dados](#banco-de-dados)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Execução](#execução)
- [Demo Online](#demo-online)
- [Testes](#testes)
- [Qualidade de Código](#qualidade-de-código)
- [Endpoints da API](#endpoints-da-api)
- [Estrutura de Resposta](#estrutura-de-resposta)
- [Autor](#autor)

## Sobre o Projeto

Sistema completo para controle de adoções de pets, permitindo cadastro de pessoas, animais e gerenciamento de adoções. O projeto foi estruturado com foco em **separação de responsabilidades**, **testabilidade** e **manutenibilidade**.

## Arquitetura

O projeto segue os princípios da **Clean Architecture**, organizando o código em camadas bem definidas:
```
PET_ADOPTION_API/
├── .vscode/                  # Configurações do VS Code
├── src/
│   ├── controllers/          # Camada de controle (regras de negócio)
│   │   ├── interfaces/       # Contratos dos controllers
│   │   ├── person_creator_controller.py
│   │   ├── person_finder_controller.py
│   │   ├── pets_delete_controller.py
│   │   └── pets_lister_controller.py
│   ├── models/               # Camada de dados
│   │   └── sqlite/
│   │       ├── entities/     # Entidades do banco de dados
│   │       ├── interfaces/   # Contratos dos repositórios
│   │       └── repositories/ # Implementação dos repositórios
│   ├── views/                # Camada de apresentação (rotas Flask)
│   │   ├── interfaces/
│   │   ├── person_creator_view.py
│   │   ├── person_finder_view.py
│   │   ├── pets_delete_view.py
│   │   └── pets_lister_view.py
│   ├── main/                 # Configurações principais
│   │   ├── composer/         # Injeção de dependências
│   │   ├── routes/           # Registro de rotas
│   │   └── server/           # Configuração do servidor Flask
│   ├── errors/               # Tratamento de erros
│   │   ├── error_types/
│   │   └── error_handler.py
│   ├── validators/           # Validadores de dados
│   └── __init__.py
├── .env/                     # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── .pre-commit-config.yaml  # Configuração de pre-commit hooks
├── .pylintrc                # Configuração do Pylint
├── case.py                  # Script auxiliar
├── ex_pylint.py             # Exemplo de uso do Pylint
├── README.md                # Documentação do projeto
├── requirements.txt         # Dependências do projeto
├── run.py                   # Script para executar a aplicação
├── storage.db               # Banco de dados SQLite
└── storage (backup).db      # Backup do banco de dados
```

### Padrões Implementados

- **Clean Architecture**: Separação em camadas (Models, Controllers, Views)
- **Repository Pattern**: Abstração da camada de dados
- **Dependency Injection**: Injeção via composer
- **MVC**: Separação entre dados, lógica e apresentação
- **SOLID Principles**: Single Responsibility e Interface Segregation

## Tecnologias

### Core
- **Python 3.10+**
- **Flask 3.1.2** - Framework web
- **SQLAlchemy 2.0.44** - ORM
- **SQLite** - Banco de dados

### Qualidade & Testes
- **Pytest 8.4.2** - Testes unitários e integração
- **Pylint 4.0.2** - Análise estática
- **Pre-commit 4.3.0** - Git hooks
- **Mock-alchemy 0.2.6** - Mocks para testes

### Utilitários
- **Pydantic 2.12.4** - Validação de dados
- **Flask-CORS 6.0.1** - Gerenciamento CORS
- **Pytest-mock 3.15.1** - Fixtures de mock

## Banco de Dados

### Modelo de Dados

O projeto utiliza **SQLite** com o seguinte schema:

#### Tabela: pets
```sql
CREATE TABLE IF NOT EXISTS 'pets' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);
```

#### Tabela: people
```sql
CREATE TABLE IF NOT EXISTS 'people' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    pet_id INTEGER NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);
```

### Relacionamentos
- **One-to-Many**: Uma pessoa pode adotar um pet (1:N entre pets e people)

### Dados de Exemplo
```sql
INSERT INTO pets (name, type)
VALUES
    ("cobra", "snake"),
    ("cao", "dog"),
    ("gato", "cat"),
    ("jorgin", "hamster"),
    ("burro", "donkey"),
    ("shrek", "ogro"),
    ("belinha", "dog");
```

### Visualização
O banco pode ser visualizado e gerenciado através do **DBeaver**.

## Funcionalidades

### Gestão de Pessoas
- **POST** `/person` - Cadastrar pessoa adotante
- **GET** `/person/{person_id}` - Buscar pessoa por ID
- Validação de nomes (apenas letras A-Z)
- Vinculação com pet via `pet_id`

### Gestão de Pets
- **GET** `/pets` - Listar todos os pets
- **DELETE** `/pets/{name}` - Remover pet por nome
- Tipos suportados: dog, cat, snake, hamster, donkey, ogro

## Instalação
```bash
# Clone o repositório
git clone https://github.com/davioliveiraes/pet_adoption_api.git
cd pet_adoption_api

# Crie e ative o ambiente virtual
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure os hooks do pre-commit (opcional)
pre-commit install
```

## Execução
```bash
# Executar a aplicação
python run.py

# Ou via Flask CLI
flask run

# Modo debug
flask run --debug
```

A API estará disponível em `http://localhost:3000`

## Demo Online

A API está disponível temporariamente no Render para fins didáticos e demonstração:

**Base URL**: `https://seu-app.onrender.com`

**Nota**: Este deploy é temporário e serve apenas para demonstração do projeto. O serviço pode estar inativo após período de inatividade (cold start).

### Testando a Demo
```bash
# Listar pets
curl https://seu-app.onrender.com/pets

# Criar pessoa
curl -X POST https://seu-app.onrender.com/person \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Maria","last_name":"Silva","age":25,"pet_id":2}'

# Buscar pessoa
curl https://seu-app.onrender.com/person/1
```

**Atenção**: O banco de dados é reiniciado periodicamente, então os dados inseridos são temporários.

## Testes
```bash
# Executar todos os testes
pytest

# Testes com verbosidade
pytest -v

# Testes com cobertura
pytest --cov=src

# Testes específicos
pytest src/controllers/
pytest src/models/
```

## Qualidade de Código
```bash
# Executar Pylint
pylint src/

# Verificar pre-commit hooks
pre-commit run --all-files
```

## Endpoints da API

### Listar Pets
**GET** `/pets`

Retorna todos os pets cadastrados no sistema.

**Request:**
```http
GET http://localhost:3000/pets
```

**Response: 200 OK**
```json
{
  "data": {
    "type": "Pets",
    "count": 5,
    "attributes": [
      {
        "id": 2,
        "name": "cao"
      },
      {
        "id": 3,
        "name": "gato"
      },
      {
        "id": 4,
        "name": "jorgin"
      },
      {
        "id": 5,
        "name": "burro"
      },
      {
        "id": 6,
        "name": "shrek"
      }
    ]
  }
}
```

---

### Criar Pessoa
**POST** `/person`

Cadastra uma nova pessoa adotante.

**Request:**
```http
POST http://localhost:3000/person
Content-Type: application/json

{
  "first_name": "Shikamara",
  "last_name": "Nara",
  "age": 27,
  "pet_id": 6
}
```

**Response: 201 Created**
```json
{
  "data": {
    "type": "Person",
    "count": 1,
    "attributes": {
      "first_name": "Shikamara",
      "last_name": "Nara",
      "age": 27,
      "pet_id": 6
    }
  }
}
```

---

### Buscar Pessoa
**GET** `/person/{person_id}`

Busca uma pessoa específica por ID.

**Request:**
```http
GET http://localhost:3000/person/1
```

**Response: 200 OK**
```json
{
  "data": {
    "type": "Person",
    "count": 1,
    "attributes": {
      "id": 1,
      "first_name": "Shikamara",
      "last_name": "Nara",
      "age": 27,
      "pet_id": 6
    }
  }
}
```

**Response: 404 Not Found**
```json
{
  "errors": [
    {
      "title": "NotFound",
      "detail": "Pessoa nao encontrada"
    }
  ]
}
```

---

### Deletar Pet
**DELETE** `/pets/{name}`

Remove um pet do sistema pelo nome.

**Request:**
```http
DELETE http://localhost:3000/pets/cobra
```

**Response: 200 OK**
```json
{
  "data": {
    "type": "Pet",
    "message": "Pet deletado com sucesso"
  }
}
```

---

## Estrutura de Resposta

### Sucesso
```json
{
  "data": {
    "type": "ResourceType",
    "count": 1,
    "attributes": {}
  }
}
```

### Erro
```json
{
  "errors": [
    {
      "title": "ErrorType",
      "detail": "Mensagem de erro detalhada"
    }
  ]
}
```

## Testando no Postman

1. **Importe os endpoints** na collection do Postman
2. **Configure a base URL**: `http://localhost:3000` ou use a demo online
3. **Endpoints disponíveis**:
   - `GET` Lister Pets
   - `POST` Create Person  
   - `GET` Finder Person
   - `DELETE` Delete Pets

## Autor

Desenvolvido por **Davi Oliveira** no curso de Python na **Rocketseat**

- LinkedIn: [Davi Oliveira](https://linkedin.com/in/davioliveiraes)

---

Se este projeto foi útil para você, considere dar uma estrela!