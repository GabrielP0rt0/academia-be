pacote “Geral” pronto para passar ao desenvolvedor (cursor): planejamento de tarefas, arquitetura de alto nível, contratos de API (endpoints + formatos JSON de exemplo), estrutura de pastas sugerida, fluxos de uso (UX), critérios de aceite e roteiro de testes locais. Tudo sem código — só direcionamento claro para implementação e primeiros testes locais.

1 — Objetivo curto-prazo

POC com backend Python (FastAPI) + front React (Vite) + arquivos JSON como "banco". Entregáveis mínimos:

CRUD de alunos

Cadastro de aulas e registro de presença

Registro de avaliações físicas e visualização por gráfico

Registro de entradas/saídas e fechamento de caixa por dia

Deploy local e instruções para testes iniciais

2 — Arquitetura de alto nível (descrição)

Client (React SPA)

Faz chamadas REST à API. Mostra dashboard, telas de alunos, avaliações, presença e caixa.

API (FastAPI)

Expondo endpoints REST para todos os recursos. Lógica de negócio, validação e agregações (ex.: total caixa por dia, dados para gráficos).

“DB” (JSON files)

Um arquivo JSON por recurso (students.json, classes.json, attendance.json, evaluations.json, finance.json, users.json).

Operações de leitura/escrita com mecanismo de lock por arquivo para evitar corrupção em acessos concorrentes.

Ambiente local

Backend roda em localhost:8000, frontend em localhost:3000 (ou porta Vite).

CI/CD (opcional para POC)

GitHub Actions para lint/tests e deploy automático do frontend (Vercel) e backend (Render/Railway) quando migrar para um DB real.

3 — Estrutura de pastas sugerida (conceitual)

/backend/

app/ — código da API

data/ — arquivos JSON (seeds)

requirements.txt, README-backend.md

/frontend/

src/ — páginas e componentes

public/ ou index.html

package.json, README-frontend.md

README.md raiz com resumo do projeto e comandos para rodar

(Entregue isso ao desenvolvedor como um checklist — ele criará os arquivos.)

4 — Modelos de dados (JSON — exemplos de formato / contrato)

Use objetos simples (IDs como string UUID ou curtos). Exemplos de campos essenciais:

students.json (lista de objetos)

{
  "id": "string",
  "name": "string",
  "birthdate": "YYYY-MM-DD",
  "phone": "string",
  "created_at": "ISO8601"
}


classes.json

{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "ISO8601"
}


attendance.json

{
  "id": "string",
  "class_id": "string",
  "student_id": "string",
  "date_time": "ISO8601",
  "status": "present"  // ou "absent"
}


evaluations.json

{
  "id": "string",
  "student_id": "string",
  "date": "YYYY-MM-DD",
  "weight_kg": number,
  "height_m": number,
  "measurements": { "waist_cm": number, "hip_cm": number, ... },
  "notes": "string"
}


finance.json

{
  "id": "string",
  "date_time": "ISO8601",
  "type": "income|expense",
  "amount": number,
  "category": "string",
  "description": "string",
  "created_by": "string"
}

5 — Contrato de API (endpoints + payloads — pronto para implementar)

(Entregue ao desenvolvedor para que implemente as rotas.)

Autenticação simples (POC)

POST /auth/login → payload { "email": "...", "password": "..." } → resposta { "token": "..." } (opcional para POC)

Students

GET /students → lista de students

POST /students → body student (sem id) → cria e retorna objeto criado

GET /students/{id} → detalhes

Classes

GET /classes

POST /classes → cria aula

Attendance

POST /attendance → body { class_id, student_id, date_time? } → adiciona registro

GET /attendance/class/{class_id}?from=&to= → lista

Evaluations

POST /evaluations → body evaluation → cria

GET /evaluations/student/{student_id} → lista por aluno

GET /evaluations/student/{student_id}/chart-data → retorna array ordenado (date, weight) pronto para gráfico (recomendado)

Finance

POST /finance → cria entry

GET /finance?date=YYYY-MM-DD → retorna entries do dia e soma total (server-side aggregation: total_income, total_expense, balance)

Dashboard

GET /dashboard/summary?date=YYYY-MM-DD → retorna { active_students, todays_classes, total_income, total_expense }

Erros e códigos: usar padrões HTTP (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error).

6 — Regras e cálculos (lógica de domínio)

IMC: calcular IMC como weight_kg / (height_m ** 2) (pode ser calculado no backend antes de salvar ou no front ao exibir).

Fechamento de caixa: backend deve somar entradas/saídas do dia e retornar totais.

Evolução (gráficos): ordenar avaliações por data; serie de peso e opcionalmente IMC.

Presença: permitir inserir por lista (array) para evitar múltiplas requisições (ex.: POST /attendance/bulk).

7 — Considerações para usar JSON como "DB" (riscos e mitigação)

Risco principal: corrupção dos arquivos por escrita concorrente.

Mitigações:

Implementar locks por arquivo (mutex) durante leitura/gravação.

Ler-modificar-gravar: sempre ler o arquivo inteiro, modificar em memória e sobrescrever atomically (escrever para arquivo temporário e renomear).

Tratar JSONDecodeError e restaurar de 'backup' (um arquivo .bak) caso o JSON esteja inválido.

Fazer backups periódicos (copiar arquivos data/*.json para data/backups/ com timestamp).

Evitar operações que demorem muito no request thread — se espera concorrência real, migrar para DB real.

Performance:

Para POC local e poucos usuários, JSON é aceitável; para múltiplos acessos simultâneos, migrar.

8 — Estrutura funcional do front (páginas e componentes)

Páginas principais:

Dashboard: resumo (total caixa do dia, alunos ativos, próximas aulas)

Alunos: lista, cadastro, detalhar (ver avaliações)

Avaliações: selecionar aluno, formulário de avaliação, gráfico de evolução

Aulas: listar, criar, abrir chamada de presença, histórico de presença

Caixa/Financeiro: registrar entrada/saída, ver fechamento diário

Componentes (recomendados):

Formulário de aluno (StudentForm)

Lista de alunos (StudentList)

Componente de gráfico (EvalChart) — recebe { labels: [], datasets: [] }

Modal de presença (AttendanceModal)

Tabela de lançamentos financeiros (FinanceTable)

UX notes:

Formularios simples, validação mínima (campos obrigatórios).

Feedback visual após ações (toast/success/error).

Botão “Gerar relatório” exporta CSV ou JSON (simples).

9 — Plano de trabalho curto-prazo para o desenvolvedor (tarefas com horas)

Total 100h (ajustado para implementação com JSON DB):

Setup & seeds + README — 6h

Criar estrutura de pastas, arquivos JSON seeds, README com comandos.

Implementar camada de acesso a JSON (locks, backups) — 10h

Funções read/write com lock, gravação atômica, backup automático.

API endpoints (CRUD básico) — 20h

Students, Classes, Attendance, Evaluations, Finance, Dashboard.

Validação & regras de negócio — 8h

IMC, agregados de caixa, filtros por data.

Frontend (páginas principais) — 30h

Dashboard, Alunos, Avaliações (com gráfico), Aulas, Caixa.

Testes locais e QA manual — 10h

Testes de fluxo, casos de borda, correções.

Documentação & scripts para rodar — 6h

README-backend, README-frontend, comandos para iniciar (venv/npm).

Buffer / ajustes finais — 10h

Total estimado: 100h

10 — Roteiro de primeiros testes locais (checklist para o cursor executar)

Clonar repo e instalar dependências backend e frontend.

Rodar backend (uvicorn) e verificar GET /docs (OpenAPI).

Verificar seed: GET /students retorna seed.

Criar um novo aluno via POST /students e confirmar leitura.

Criar aula (POST /classes) e marcar 2 presenças (bulk).

Criar 3 avaliações para um aluno e confirmar GET /evaluations/student/{id} retorna ordenado por data.

Verificar gráfico no front: selecionar aluno, ver 3 pontos.

Adicionar 3 lançamentos financeiros (2 incomes, 1 expense) e chamar GET /finance?date=YYYY-MM-DD → conferir total.

Testar concorrência simples (duas requisições de escrita ao mesmo tempo) e checar se arquivos JSON ficaram íntegros.

Simular corrupção: manualmente alterar JSON para inválido e checar recuperação por backup.

Critério de aceite mínimo: todos os passos acima funcionam sem corromper os arquivos e sem erros 500.

11 — CI / Deploy (para quando quiser publicar)

Frontend: conectar repositório ao Vercel (deploy grátis para sites estáticos).

Backend: provider com plano free (Render / Railway). Para POC com JSON files, é mais seguro manter backend como container (Docker) e montar volume persistente — atenção: providers free podem não manter arquivos locais após restart → não usar JSON-DB em produção. Para POC em ambiente público, preferir usar SQLite ou banco cloud gratuito (Supabase) quando precisar persistência estável.

12 — Segurança e boas práticas mínimas

Não salvar senhas em texto (para POC, pode haver login fake).

Validar e sanitizar entradas (pydantic).

Habilitar CORS apenas para origem do front (durante desenvolvimento * ok).

Fazer backup automático dos JSONs antes de qualquer gravação (timestamped copy).

13 — Critérios de sucesso da POC (para apresentar à academia)

Caixa: fechamento diário correto (totais e extrato) verificado com pelo menos 5 lançamentos.

Avaliações: aluno consegue ver gráfico de evolução com 3+ avaliações.

Presença: instrutor consegue abrir chamada e registrar lista de presenças sem erro.

Usabilidade: gestores conseguem usar as telas principais sem auxílio após uma demonstração de 10 minutos.

Estabilidade: arquivos JSON não corrompem durante uso normal (testes de concorrência básicos).

14 — Próximos passos após a POC (recomendado)

Migrar para Postgres (Supabase free) quando validar o fluxo.

Adicionar autenticação real (Supabase Auth / Firebase).

Exportar relatórios em PDF/CSV para gestão.

Versionar backups e adicionar monitoramento (logs, erros).

15 — Entregáveis que você deve receber do cursor (ao entregar POC)

Repositório Git com commits claros.

README com instruções de setup e testes.

Seeds JSON em /backend/data/.

Endpoints funcionando (lista de URLs).

Vídeo curto (3–5 min) demonstrando os fluxos: cadastro aluno, avaliação, gráfico, presença e fechamento de caixa.

Relatório curto (1–2 páginas) com problemas encontrados e recomendações.