# Academia Digital - Backend API

Backend API desenvolvido com FastAPI para o sistema de gestão de academia. Esta é uma POC (Proof of Concept) que utiliza arquivos JSON como banco de dados local.

## 📋 Índice

- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Execução](#execução)
- [Deploy no Render](#deploy-no-render)
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

## 🚀 Deploy no Render

### Pré-requisitos

- Conta no [Render](https://render.com)
- Repositório Git (GitHub, GitLab ou Bitbucket) com o código do projeto

### Passo a Passo

1. **Faça login no Render** e acesse o dashboard

2. **Crie um novo Web Service**:
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório Git
   - Selecione o repositório do projeto

3. **Configure o serviço**:
   - **Name**: `academia-be` (ou o nome que preferir)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Escolha o plano (Free para testes)

4. **Variáveis de Ambiente** (opcional, mas recomendado):
   - `ENVIRONMENT`: `production`
   - `ALLOWED_ORIGINS`: URLs permitidas separadas por vírgula (ex: `https://seu-frontend.com`)
   - `PORT`: Deixe vazio (Render define automaticamente)

5. **Deploy**:
   - Clique em "Create Web Service"
   - O Render irá fazer o build e deploy automaticamente
   - Aguarde o processo concluir (pode levar alguns minutos)

6. **Verificação**:
   - Após o deploy, acesse a URL fornecida pelo Render
   - Teste o endpoint `/health` para verificar se está funcionando
   - Acesse `/docs` para ver a documentação da API

### Configuração Automática com render.yaml

O projeto já inclui um arquivo `render.yaml` que configura automaticamente o serviço. Se você usar este arquivo:

1. No Render, ao criar o serviço, selecione "Apply render.yaml"
2. O Render lerá as configurações do arquivo automaticamente
3. Você ainda pode ajustar variáveis de ambiente manualmente se necessário

### Variáveis de Ambiente Recomendadas

Para produção, configure as seguintes variáveis no Render:

```env
ENVIRONMENT=production
ALLOWED_ORIGINS=https://seu-frontend.com,https://www.seu-frontend.com
```

**Importante**: 
- Substitua `seu-frontend.com` pela URL real do seu frontend
- Se não configurar `ALLOWED_ORIGINS`, o CORS permitirá todas as origens (não recomendado para produção)

### Troubleshooting do Deploy

**Erro de build**:
- Verifique se o `requirements.txt` está atualizado
- Confirme que todas as dependências estão listadas

**Erro ao iniciar**:
- Verifique os logs no dashboard do Render
- Confirme que o `startCommand` está correto
- Verifique se a porta está usando `$PORT` (variável do Render)

**CORS não funciona**:
- Configure `ALLOWED_ORIGINS` com as URLs corretas do frontend
- Certifique-se de que `ENVIRONMENT=production` está configurado

**Dados não persistem**:
- ⚠️ **Atenção**: No Render, os arquivos JSON são armazenados no sistema de arquivos efêmero
- Os dados serão perdidos quando o serviço reiniciar ou for atualizado
- Para produção, considere migrar para um banco de dados persistente (PostgreSQL, MongoDB, etc.)

### Limitações do Deploy com JSON

Como este projeto usa arquivos JSON como banco de dados:

- **Dados temporários**: No Render, os dados são perdidos quando o serviço reinicia
- **Não escalável**: Não funciona bem com múltiplas instâncias
- **Adequado apenas para**: POC, testes e desenvolvimento

**Recomendação**: Para produção, migre para um banco de dados real antes de fazer deploy.

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

