Especificação do Backend — POC Academia Digital

Stack: Python + FastAPI + JSON Files (como DB)
Objetivo: Criar uma API funcional e estável para a POC, usando arquivos JSON como banco de dados local, com estrutura simples e clara para futura migração para um banco real (Postgres/Supabase).

1. Objetivo do Backend

O backend deve fornecer uma API REST simples e organizada, responsável por:

Persistência de dados (em arquivos JSON, um por recurso).

Regras de negócio (fluxo de caixa, cálculo de IMC, presença, avaliações).

Validação mínima de dados.

Retorno de dados prontos para consumo do frontend (React).

Endpoints compatíveis com padrões modernos (HTTP status codes, JSON limpo, consistência em campos).

O backend será responsável por criar, listar, atualizar e agregar informações necessárias para o front gerar telas, tabelas e gráficos.

2. Arquitetura
backend/
├─ app/
│  ├─ main.py            # inicialização da API
│  ├─ schemas.py         # modelos Pydantic (para validar inputs e outputs)
│  ├─ crud.py            # operações de leitura e escrita em JSON + lógica CRUD
│  ├─ db.py              # funções de leitura/escrita em JSON com lock
│  ├─ utils.py           # funções auxiliares (cálculo IMC, agregações)
│  └─ data/              # “banco de dados” JSON
│     ├─ students.json
│     ├─ classes.json
│     ├─ attendance.json
│     ├─ evaluations.json
│     ├─ finance.json
│     └─ users.json
├─ requirements.txt
└─ README.md

3. Estrutura dos arquivos JSON (DB)

Cada arquivo JSON deve conter uma lista de objetos, nunca um objeto único.

students.json
[
  {
    "id": "uuid",
    "name": "string",
    "birthdate": "YYYY-MM-DD",
    "phone": "string",
    "created_at": "ISO8601"
  }
]

classes.json
[
  {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "created_at": "ISO8601"
  }
]

attendance.json
[
  {
    "id": "uuid",
    "class_id": "uuid",
    "student_id": "uuid",
    "date_time": "ISO8601",
    "status": "present"
  }
]

evaluations.json
[
  {
    "id": "uuid",
    "student_id": "uuid",
    "date": "YYYY-MM-DD",
    "weight_kg": 70.2,
    "height_m": 1.70,
    "measurements": {
      "waist_cm": 80,
      "hip_cm": 95
    },
    "notes": "string"
  }
]

finance.json
[
  {
    "id": "uuid",
    "date_time": "ISO8601",
    "type": "income",
    "amount": 100.00,
    "category": "Mensalidade",
    "description": "Janeiro"
  }
]

4. Regras para manipulação dos JSON (OBRIGATÓRIO)
4.1 Confiabilidade

Todas as operações de leitura/escrita devem:

Usar lock por arquivo para evitar corrupção.

Fazer backup automático antes da escrita:

Ex: criar um arquivo.json.bak antes de sobrescrever.

Usar escrita “atômica”:

Escrever em um arquivo temporário e renomear.

4.2 Integridade

IDs sempre string (uuid4).

Campos opcionais devem existir no JSON com valor null quando aplicável.

4.3 Tratamento de erros

JSON malformado → restaurar .bak.

Dados inválidos → retornar HTTP 400 com mensagem clara.

Item não encontrado → HTTP 404.

5. Schemas (Pydantic)

O cursor deve criar schemas equivalentes a estes:

StudentCreate
name: str
birthdate: str|None
phone: str|None

EvaluationCreate
student_id: str
weight_kg: float
height_m: float|None
measurements: dict|None
notes: str|None

FinanceEntryCreate
type: "income"|"expense"
amount: float
category: str|None
description: str|None

6. Endpoints da API (contratos)

Todos os endpoints devem retornar JSON.

6.1 Students
GET /students

Retorna lista de alunos.

POST /students

Payload:

{
  "name": "João",
  "birthdate": "1990-01-01",
  "phone": "99999999"
}


Retorna aluno criado com id.

GET /students/{id}

Retorna aluno específico.

6.2 Classes
GET /classes
POST /classes

Payload:

{
  "name": "Funcional",
  "description": "Treino de resistência"
}

6.3 Attendance
POST /attendance

Payload:

{
  "class_id": "c1",
  "student_id": "s1",
  "status": "present"
}

GET /attendance/class/{class_id}

Retorna registros daquela aula.

6.4 Evaluations
POST /evaluations

Payload:

{
  "student_id": "s1",
  "weight_kg": 80,
  "height_m": 1.75,
  "measurements": { "waist_cm": 82 },
  "notes": "Início"
}

GET /evaluations/student/{student_id}

Lista avaliações.

GET /evaluations/student/{id}/chart-data

Retorna dados ordenados por data:

{
  "labels": ["2025-01-01", "2025-02-01"],
  "weights": [80, 78],
  "imc": [26.1, 25.5]
}

6.5 Finance (Fechamento de Caixa)
POST /finance

Payload:

{
  "type": "income",
  "amount": 120,
  "category": "Mensalidade",
  "description": "Fevereiro"
}

GET /finance?date=YYYY-MM-DD

Retorna:

{
  "entries": [...],
  "total_income": 300,
  "total_expense": 100,
  "balance": 200
}

6.6 Dashboard
GET /dashboard/summary

Retorna:

{
  "active_students": 45,
  "today_classes": 3,
  "total_income_today": 300,
  "total_expense_today": 100
}

7. Regras de negócio
Students

Nome obrigatório.

birthdate e phone opcionais.

Evaluations

Se height_m existir → calcular IMC.

Ordenar por data quando listar.

Finance

type ∈ {income, expense}

amount > 0

Fechamento diário calculado no servidor.

Attendance

Registrar presente/ausente.

Usar horário atual se não for enviado.

8. Critérios de Aceite (Checklist)
Arquitetura:

 Pasta app/data com arquivos JSON válidos.

 Operações JSON com lock e backup.

 Módulo CRUD separado da camada de roteamento.

API:

 Todos os endpoints implementados.

 Todos retornam JSON válido.

 Códigos HTTP adequados (201 para criação, 404 quando necessário).

Regras de negócio:

 IMC calculado corretamente.

 Fechamento de caixa funcionando com totalizações.

 Avaliações ordenadas.

Qualidade:

 API documentada automaticamente em /docs.

 Testes manuais concluídos conforme roteiro.

 JSONs permanecem íntegros após múltiplas escritas.

9. Roteiro de Testes Locais (para validar a entrega)

Instalar dependências (pip install -r requirements.txt).

Rodar a API (uvicorn app.main:app --reload).

Criar aluno → POST /students.

Listar alunos → GET /students.

Criar aula → POST /classes.

Adicionar presença → POST /attendance.

Criar 3 avaliações para um aluno.

Verificar GET /evaluations/student/{id}/chart-data.

Criar lançamentos financeiros.

Testar fechamento diário.

Verificar se os arquivos JSON não corromperam.

10. Futuras melhorias (fora escopo da POC)

Migrar JSON → SQLite ou Postgres.

Implementar autenticação real (JWT/Supabase Auth).

Relatórios PDF.

Auditoria de alterações (log).