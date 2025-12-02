# Academia Digital - Backend API

Backend API desenvolvido com FastAPI para o sistema de gestão de academia. Esta é uma POC (Proof of Concept) que utiliza arquivos JSON como banco de dados local.

## 📋 Índice

- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Execução](#execução)
- [Endpoints da API](#endpoints-da-api)
- [Testes](#testes)
- [Arquitetura](#arquitetura)
- [Notas Importantes](#notas-importantes)

## 🛠 Tecnologias

- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **JSON Files** - Armazenamento de dados (POC)

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── db.py                # Camada de acesso a JSON (locks, backups)
│   ├── schemas.py           # Modelos Pydantic (validação)
│   ├── crud.py              # Operações CRUD
│   ├── utils.py             # Funções auxiliares (IMC, agregações)
│   ├── data/                # Arquivos JSON (banco de dados)
│   │   ├── students.json
│   │   ├── classes.json
│   │   ├── attendance.json
│   │   ├── evaluations.json
│   │   ├── finance.json
│   │   ├── users.json
│   │   └── backups/         # Backups automáticos
│   └── routers/             # Rotas da API
│       ├── __init__.py
│       ├── auth.py
│       ├── students.py
│       ├── classes.py
│       ├── attendance.py
│       ├── evaluations.py
│       ├── finance.py
│       └── dashboard.py
├── requirements.txt
└── README.md
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório** (se aplicável)

2. **Crie um ambiente virtual** (recomendado):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

## ▶️ Execução

### Modo Desenvolvimento (com reload automático)

```bash
uvicorn app.main:app --reload
```

### Modo Produção

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints da API

### Autenticação

- `POST /api/auth/login` - Login (hardcoded para POC)
  - Credenciais: `admin@academia.com` / `admin123`

### Students (Alunos)

- `GET /api/students` - Lista todos os alunos
- `GET /api/students/{id}` - Obtém aluno por ID
- `POST /api/students` - Cria novo aluno

### Classes (Aulas)

- `GET /api/classes` - Lista todas as aulas
- `POST /api/classes` - Cria nova aula

### Attendance (Presença)

- `POST /api/attendance` - Registra presença individual
- `POST /api/attendance/bulk` - Registra múltiplas presenças
- `GET /api/attendance/class/{class_id}?from=YYYY-MM-DD&to=YYYY-MM-DD` - Lista presenças de uma aula (com filtro opcional de data)

### Evaluations (Avaliações)

- `POST /api/evaluations` - Cria nova avaliação física
- `GET /api/evaluations/student/{student_id}` - Lista avaliações de um aluno
- `GET /api/evaluations/student/{student_id}/chart-data` - Dados para gráfico de evolução

### Finance (Financeiro)

- `POST /api/finance` - Cria lançamento financeiro
- `GET /api/finance?date=YYYY-MM-DD` - Lista lançamentos do dia com totais

### Dashboard

- `GET /api/dashboard/summary?date=YYYY-MM-DD` - Resumo do dashboard

## 🧪 Testes

### Roteiro de Testes Básicos

1. **Verificar API está rodando**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Acessar documentação**:
   - Abra http://localhost:8000/docs no navegador

3. **Testar login**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@academia.com", "password": "admin123"}'
   ```

4. **Listar alunos**:
   ```bash
   curl http://localhost:8000/api/students
   ```

5. **Criar novo aluno**:
   ```bash
   curl -X POST http://localhost:8000/api/students \
     -H "Content-Type: application/json" \
     -d '{"name": "Teste Aluno", "birthdate": "1995-01-01", "phone": "11999999999"}'
   ```

6. **Criar aula**:
   ```bash
   curl -X POST http://localhost:8000/api/classes \
     -H "Content-Type: application/json" \
     -d '{"name": "Pilates", "description": "Aula de pilates"}'
   ```

7. **Registrar presença**:
   ```bash
   curl -X POST http://localhost:8000/api/attendance \
     -H "Content-Type: application/json" \
     -d '{"class_id": "ID_DA_AULA", "student_id": "ID_DO_ALUNO", "status": "present"}'
   ```

8. **Criar avaliação**:
   ```bash
   curl -X POST http://localhost:8000/api/evaluations \
     -H "Content-Type: application/json" \
     -d '{"student_id": "ID_DO_ALUNO", "date": "2025-01-12", "weight_kg": 75.5, "height_m": 1.70, "notes": "Avaliação inicial"}'
   ```

9. **Verificar gráfico de evolução**:
   ```bash
   curl http://localhost:8000/api/evaluations/student/ID_DO_ALUNO/chart-data
   ```

10. **Criar lançamento financeiro**:
    ```bash
    curl -X POST http://localhost:8000/api/finance \
      -H "Content-Type: application/json" \
      -d '{"type": "income", "amount": 150.00, "category": "Mensalidade", "description": "Janeiro"}'
    ```

11. **Verificar fechamento de caixa**:
    ```bash
    curl http://localhost:8000/api/finance?date=2025-01-12
    ```

12. **Verificar dashboard**:
    ```bash
    curl http://localhost:8000/api/dashboard/summary?date=2025-01-12
    ```

## 🏗 Arquitetura

### Camadas

1. **Routers** (`app/routers/`) - Endpoints HTTP, validação de entrada
2. **CRUD** (`app/crud.py`) - Lógica de negócio e operações de dados
3. **Database Layer** (`app/db.py`) - Acesso seguro a arquivos JSON
4. **Schemas** (`app/schemas.py`) - Validação e serialização de dados
5. **Utils** (`app/utils.py`) - Funções auxiliares (cálculos, formatação)

### Segurança de Dados

- **Locks por arquivo**: Previne corrupção em acessos concorrentes
- **Backups automáticos**: Cria `.bak` antes de cada escrita
- **Escrita atômica**: Escreve em arquivo temporário e renomeia
- **Recuperação**: Restaura automaticamente de backup se JSON estiver corrompido

## ⚠️ Notas Importantes

### POC - Limitações

- **JSON como DB**: Adequado apenas para POC e desenvolvimento local
- **Autenticação hardcoded**: Não usar em produção
- **CORS aberto**: Configurado para `*` (restringir em produção)
- **Sem migração de dados**: Arquivos JSON não têm versionamento

### Migração Futura

Para produção, recomenda-se migrar para:
- **Banco de dados**: PostgreSQL (Supabase) ou SQLite
- **Autenticação**: JWT tokens ou Supabase Auth
- **CORS**: Configurar origens específicas
- **Backups**: Sistema de versionamento de dados

### Performance

- Adequado para poucos usuários simultâneos
- Para múltiplos acessos concorrentes, migrar para banco de dados real
- Arquivos JSON podem ficar lentos com muitos registros (>1000)

## 📝 Exemplos de Uso

### Criar aluno e avaliação completa

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Criar aluno
student = requests.post(f"{BASE_URL}/students", json={
    "name": "João Silva",
    "birthdate": "1990-05-15",
    "phone": "11999999999"
}).json()

student_id = student["id"]

# Criar avaliação
evaluation = requests.post(f"{BASE_URL}/evaluations", json={
    "student_id": student_id,
    "date": "2025-01-12",
    "weight_kg": 80.5,
    "height_m": 1.75,
    "notes": "Avaliação inicial"
}).json()

# Obter dados para gráfico
chart_data = requests.get(f"{BASE_URL}/evaluations/student/{student_id}/chart-data").json()
print(chart_data)
```

## 🔧 Troubleshooting

### Erro ao iniciar

- Verifique se a porta 8000 está livre
- Certifique-se de que todas as dependências estão instaladas
- Verifique se os arquivos JSON em `app/data/` existem e são válidos

### Erro de permissão

- Verifique permissões de escrita na pasta `app/data/`
- Certifique-se de que o usuário tem permissão para criar arquivos

### JSON corrompido

- O sistema tenta restaurar automaticamente do backup `.bak`
- Se necessário, restaure manualmente de `app/data/backups/`

## 📄 Licença

Este projeto é uma POC para fins de demonstração.

## 👤 Autor

Desenvolvido para Academia Digital - POC Backend

