# Guia de Integração Frontend - Academia Digital API

Este documento fornece todas as informações necessárias para integrar o frontend React com a API backend FastAPI.

## 📋 Índice

- [Informações Gerais](#informações-gerais)
- [Configuração Base](#configuração-base)
- [Autenticação](#autenticação)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Exemplos de Código](#exemplos-de-código)
- [Tratamento de Erros](#tratamento-de-erros)
- [Estruturas de Dados](#estruturas-de-dados)
- [Boas Práticas](#boas-práticas)
- [Checklist de Integração](#checklist-de-integração)

## 🔧 Informações Gerais

### URL Base da API

```
http://localhost:8000/api
```

### Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Formato de Dados

- **Content-Type**: `application/json`
- **Accept**: `application/json`
- Todas as requisições e respostas são em JSON

### Códigos HTTP

- `200 OK` - Sucesso (GET, PUT)
- `201 Created` - Recurso criado com sucesso (POST)
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro no servidor

## ⚙️ Configuração Base

### Exemplo de Configuração Axios

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token (quando implementar autenticação real)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirecionar para login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Exemplo de Configuração Fetch

```typescript
// src/services/api.ts
const API_BASE_URL = 'http://localhost:8000/api';

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    const error = await response.json();
    throw new Error(error.detail || 'Erro na requisição');
  }

  return response.json();
}

export default apiRequest;
```

## 🔐 Autenticação

### Login

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "admin@academia.com",
  "password": "admin123"
}
```

**Response** (200 OK):
```json
{
  "token": "hardcoded_token_for_poc_12345",
  "message": "Login successful"
}
```

**Exemplo de Código**:
```typescript
// src/services/authService.ts
import api from './api';

interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  token: string;
  message: string;
}

export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>('/auth/login', credentials);
  localStorage.setItem('token', response.data.token);
  return response.data;
};
```

## 📡 Endpoints Disponíveis

### Students (Alunos)

#### Listar Todos os Alunos

**GET** `/api/students`

**Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "João Silva",
    "birthdate": "1990-05-15",
    "phone": "11999999999",
    "created_at": "2025-01-01T10:00:00"
  }
]
```

**Exemplo de Código**:
```typescript
// src/services/studentService.ts
import api from './api';

export interface Student {
  id: string;
  name: string;
  birthdate: string | null;
  phone: string | null;
  created_at: string;
}

export const getStudents = async (): Promise<Student[]> => {
  const response = await api.get<Student[]>('/students');
  return response.data;
};
```

#### Obter Aluno por ID

**GET** `/api/students/{id}`

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "João Silva",
  "birthdate": "1990-05-15",
  "phone": "11999999999",
  "created_at": "2025-01-01T10:00:00"
}
```

**Exemplo de Código**:
```typescript
export const getStudentById = async (id: string): Promise<Student> => {
  const response = await api.get<Student>(`/students/${id}`);
  return response.data;
};
```

#### Criar Novo Aluno

**POST** `/api/students`

**Request Body**:
```json
{
  "name": "Maria Santos",
  "birthdate": "1992-08-20",
  "phone": "11988888888"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Maria Santos",
  "birthdate": "1992-08-20",
  "phone": "11988888888",
  "created_at": "2025-01-12T20:30:00"
}
```

**Exemplo de Código**:
```typescript
export interface StudentCreate {
  name: string;
  birthdate?: string | null;
  phone?: string | null;
}

export const createStudent = async (data: StudentCreate): Promise<Student> => {
  const response = await api.post<Student>('/students', data);
  return response.data;
};
```

### Classes (Aulas)

#### Listar Todas as Aulas

**GET** `/api/classes`

**Response** (200 OK):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "name": "Funcional",
    "description": "Treino de resistência e funcional",
    "created_at": "2025-01-01T08:00:00"
  }
]
```

#### Criar Nova Aula

**POST** `/api/classes`

**Request Body**:
```json
{
  "name": "Pilates",
  "description": "Aula de pilates mat"
}
```

**Exemplo de Código**:
```typescript
// src/services/classService.ts
import api from './api';

export interface Class {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

export interface ClassCreate {
  name: string;
  description?: string | null;
}

export const getClasses = async (): Promise<Class[]> => {
  const response = await api.get<Class[]>('/classes');
  return response.data;
};

export const createClass = async (data: ClassCreate): Promise<Class> => {
  const response = await api.post<Class>('/classes', data);
  return response.data;
};
```

### Enrollments (Matrículas)

#### Listar Todas as Matrículas

**GET** `/api/enrollments`

**Response** (200 OK):
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "student_id": "550e8400-e29b-41d4-a716-446655440000",
    "class_id": "660e8400-e29b-41d4-a716-446655440000",
    "enrolled_at": "2025-01-12T10:00:00"
  }
]
```

#### Matricular Aluno em Aula

**POST** `/api/enrollments`

**Request Body**:
```json
{
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "class_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

**Response** (201 Created):
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "class_id": "660e8400-e29b-41d4-a716-446655440000",
  "enrolled_at": "2025-01-12T10:00:00"
}
```

#### Listar Alunos Matriculados em uma Aula

**GET** `/api/enrollments/class/{class_id}/students`

**Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "João Silva",
    "birthdate": "1990-05-15",
    "phone": "11999999999",
    "created_at": "2025-01-01T10:00:00"
  }
]
```

#### Listar Matrículas de um Aluno

**GET** `/api/enrollments/student/{student_id}`

#### Remover Matrícula

**DELETE** `/api/enrollments/{enrollment_id}`

ou

**DELETE** `/api/enrollments/student/{student_id}/class/{class_id}`

**Exemplo de Código**:
```typescript
// src/services/enrollmentService.ts
import api from './api';

export interface Enrollment {
  id: string;
  student_id: string;
  class_id: string;
  enrolled_at: string;
}

export interface EnrollmentCreate {
  student_id: string;
  class_id: string;
}

export const enrollStudent = async (data: EnrollmentCreate): Promise<Enrollment> => {
  const response = await api.post<Enrollment>('/enrollments', data);
  return response.data;
};

export const getEnrolledStudents = async (classId: string): Promise<Student[]> => {
  const response = await api.get<Student[]>(`/enrollments/class/${classId}/students`);
  return response.data;
};

export const removeEnrollment = async (enrollmentId: string): Promise<void> => {
  await api.delete(`/enrollments/${enrollmentId}`);
};
```

### Attendance (Presença)

#### Registrar Presença Individual

**POST** `/api/attendance`

**Request Body**:
```json
{
  "class_id": "660e8400-e29b-41d4-a716-446655440000",
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "present",
  "date_time": "2025-01-12T18:00:00"
}
```

**Nota**: `date_time` é opcional. Se não fornecido, usa o horário atual.

#### Registrar Múltiplas Presenças (Bulk)

**POST** `/api/attendance/bulk`

**Request Body**:
```json
{
  "entries": [
    {
      "class_id": "660e8400-e29b-41d4-a716-446655440000",
      "student_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "present"
    },
    {
      "class_id": "660e8400-e29b-41d4-a716-446655440000",
      "student_id": "550e8400-e29b-41d4-a716-446655440001",
      "status": "present"
    }
  ]
}
```

#### Listar Alunos Matriculados para Presença

**GET** `/api/attendance/class/{class_id}/students`

**Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "João Silva",
    "birthdate": "1990-05-15",
    "phone": "11999999999",
    "created_at": "2025-01-01T10:00:00"
  }
]
```

**Nota**: Este endpoint retorna apenas alunos matriculados na aula. Use este endpoint para obter a lista de alunos ao marcar presença.

#### Listar Presenças de uma Aula

**GET** `/api/attendance/class/{class_id}?from=YYYY-MM-DD&to=YYYY-MM-DD`

**Nota**: Ao criar presença, o sistema valida automaticamente se o aluno está matriculado na aula.

**Query Parameters** (opcionais):
- `from`: Data inicial (YYYY-MM-DD)
- `to`: Data final (YYYY-MM-DD)

**Exemplo de Código**:
```typescript
// src/services/attendanceService.ts
import api from './api';

export interface Attendance {
  id: string;
  class_id: string;
  student_id: string;
  date_time: string;
  status: 'present' | 'absent';
}

export interface AttendanceCreate {
  class_id: string;
  student_id: string;
  status: 'present' | 'absent';
  date_time?: string;
}

export const createAttendance = async (data: AttendanceCreate): Promise<Attendance> => {
  const response = await api.post<Attendance>('/attendance', data);
  return response.data;
};

export const createAttendanceBulk = async (
  entries: AttendanceCreate[]
): Promise<Attendance[]> => {
  const response = await api.post<Attendance[]>('/attendance/bulk', { entries });
  return response.data;
};

export const getAttendanceByClass = async (
  classId: string,
  fromDate?: string,
  toDate?: string
): Promise<Attendance[]> => {
  const params = new URLSearchParams();
  if (fromDate) params.append('from', fromDate);
  if (toDate) params.append('to', toDate);
  
  const queryString = params.toString();
  const url = `/attendance/class/${classId}${queryString ? `?${queryString}` : ''}`;
  
  const response = await api.get<Attendance[]>(url);
  return response.data;
};
```

### Evaluations (Avaliações)

#### Criar Nova Avaliação

**POST** `/api/evaluations`

**Request Body** (todos os campos são obrigatórios):
```json
{
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "date": "2025-01-12",
  "weight_kg": 80.5,
  "height_m": 1.75,
  "cardiopathy": false,
  "cardiopathy_notes": null,
  "hypertension": false,
  "hypertension_notes": null,
  "diabetes": false,
  "diabetes_notes": null,
  "heart_rate_rest": 72,
  "wells_sit_reach_test": 25.5,
  "trunk_flexion_test": 30.0,
  "skinfold_triceps": 12.5,
  "skinfold_subscapular": 15.0,
  "skinfold_subaxillary": 10.0,
  "skinfold_suprailiac": 18.0,
  "skinfold_abdominal": 20.0,
  "skinfold_quadriceps": 14.0,
  "skinfold_calf": 8.0,
  "perimeter_chest": 100.0,
  "perimeter_arm_r": 32.0,
  "perimeter_arm_l": 31.5,
  "perimeter_arm_contracted_r": 35.0,
  "perimeter_arm_contracted_l": 34.5,
  "perimeter_forearm_r": 28.0,
  "perimeter_forearm_l": 27.5,
  "perimeter_waist": 85.0,
  "perimeter_abdominal": 90.0,
  "perimeter_hip": 95.0,
  "perimeter_thigh_r": 55.0,
  "perimeter_thigh_l": 54.5,
  "perimeter_leg_r": 38.0,
  "perimeter_leg_l": 37.5,
  "notes": "Avaliação inicial completa"
}
```

**Nota**: Todos os cálculos (IMC, metabolismo basal, % gordura, etc.) são calculados automaticamente pelo backend. A idade é calculada automaticamente a partir da data de nascimento do aluno.

#### Listar Avaliações de um Aluno

**GET** `/api/evaluations/student/{student_id}`

**Response** (200 OK): Retorna lista completa com todos os campos e cálculos.

#### Obter Relatório Final de Avaliação

**GET** `/api/evaluations/{evaluation_id}/report`

**Response** (200 OK):
```json
{
  "evaluation": {
    "id": "880e8400-e29b-41d4-a716-446655440000",
    "student_id": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-01-12",
    "age": 34,
    "weight_kg": 80.5,
    "height_m": 1.75,
    "imc": 26.29,
    "basal_metabolism": 1850.5,
    "body_age": 36.2,
    "visceral_fat": 8.5,
    "fat_weight": 16.1,
    "lean_weight": 64.4,
    "fat_percentage": 20.0,
    "lean_mass_percentage": 80.0,
    ...
  },
  "student": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "João Silva",
    ...
  },
  "summary": {
    "current_date": "2025-01-12",
    "evaluation_number": 3,
    "total_evaluations": 5,
    "key_metrics": {...},
    "health_conditions": {...},
    "comparison_with_previous": {
      "previous_date": "2024-12-01",
      "weight_change_kg": -2.5,
      "imc_change": -0.8,
      "fat_percentage_change": -1.5,
      "trend": "improving"
    }
  }
}
```

**Nota**: Este endpoint retorna um relatório completo com comparações com avaliações anteriores.

#### Obter Dados para Gráfico

**GET** `/api/evaluations/student/{student_id}/chart-data`

**Response** (200 OK):
```json
{
  "labels": ["2025-01-01", "2025-01-15"],
  "weights": [80.5, 79.0],
  "imc": [26.29, 25.8]
}
```

**Exemplo de Código**:
```typescript
// src/services/evaluationService.ts
import api from './api';

export interface Evaluation {
  id: string;
  student_id: string;
  date: string;
  weight_kg: number;
  height_m: number | null;
  measurements: Record<string, number> | null;
  notes: string | null;
  imc: number | null;
}

export interface EvaluationCreate {
  student_id: string;
  date: string;
  weight_kg: number;
  height_m?: number | null;
  measurements?: Record<string, number> | null;
  notes?: string | null;
}

export interface ChartData {
  labels: string[];
  weights: number[];
  imc: (number | null)[];
}

export const createEvaluation = async (data: EvaluationCreate): Promise<Evaluation> => {
  const response = await api.post<Evaluation>('/evaluations', data);
  return response.data;
};

export const getEvaluationsByStudent = async (studentId: string): Promise<Evaluation[]> => {
  const response = await api.get<Evaluation[]>(`/evaluations/student/${studentId}`);
  return response.data;
};

export const getChartData = async (studentId: string): Promise<ChartData> => {
  const response = await api.get<ChartData>(`/evaluations/student/${studentId}/chart-data`);
  return response.data;
};
```

**Exemplo de Uso com Chart.js**:
```typescript
import { getChartData } from './services/evaluationService';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const renderChart = async (studentId: string) => {
  const chartData = await getChartData(studentId);
  
  const ctx = document.getElementById('chart') as HTMLCanvasElement;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: 'Peso (kg)',
          data: chartData.weights,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        },
        {
          label: 'IMC',
          data: chartData.imc,
          borderColor: 'rgb(255, 99, 132)',
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
};
```

### Finance (Financeiro)

#### Criar Lançamento Financeiro

**POST** `/api/finance`

**Request Body**:
```json
{
  "type": "income",
  "amount": 150.00,
  "payment_method": "pix",
  "category": "Mensalidade",
  "description": "Mensalidade Janeiro - João Silva",
  "date_time": "2025-01-12T10:00:00"
}
```

**Métodos de Pagamento**: `credit`, `debit`, `pix`, `cash`, `other`

**Nota**: `payment_method` é obrigatório. `date_time` é opcional. Se não fornecido, usa o horário atual.

#### Obter Fechamento de Caixa

**GET** `/api/finance?date=YYYY-MM-DD`

**Response** (200 OK):
```json
{
  "entries": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "date_time": "2025-01-12T10:00:00",
      "type": "income",
      "amount": 150.00,
      "payment_method": "pix",
      "category": "Mensalidade",
      "description": "Mensalidade Janeiro - João Silva",
      "created_by": null
    }
  ],
  "total_income": 150.00,
  "total_expense": 0.00,
  "balance": 150.00
}
```

#### Exportar Fluxo de Caixa para Excel

**GET** `/api/finance/export/xlsx?date=YYYY-MM-DD`

**Response**: Arquivo Excel (.xlsx) para download

**Nota**: O arquivo Excel contém todos os campos do relatório formatado, incluindo totais e saldo.

**Query Parameters**:
- `date`: Data no formato YYYY-MM-DD (opcional, usa data atual se não fornecido)

**Response** (200 OK):
```json
{
  "entries": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "date_time": "2025-01-12T10:00:00",
      "type": "income",
      "amount": 150.00,
      "category": "Mensalidade",
      "description": "Mensalidade Janeiro",
      "created_by": "admin"
    }
  ],
  "total_income": 300.00,
  "total_expense": 50.00,
  "balance": 250.00
}
```

**Exemplo de Código**:
```typescript
// src/services/financeService.ts
import api from './api';

export interface FinanceEntry {
  id: string;
  date_time: string;
  type: 'income' | 'expense';
  amount: number;
  payment_method: 'credit' | 'debit' | 'pix' | 'cash' | 'other';
  category: string | null;
  description: string | null;
  created_by: string | null;
}

export interface FinanceEntryCreate {
  type: 'income' | 'expense';
  amount: number;
  payment_method: 'credit' | 'debit' | 'pix' | 'cash' | 'other';
  category?: string | null;
  description?: string | null;
  date_time?: string;
}

export interface FinanceSummary {
  entries: FinanceEntry[];
  total_income: number;
  total_expense: number;
  balance: number;
}

export const createFinanceEntry = async (
  data: FinanceEntryCreate
): Promise<FinanceEntry> => {
  const response = await api.post<FinanceEntry>('/finance', data);
  return response.data;
};

export const getFinanceSummary = async (date?: string): Promise<FinanceSummary> => {
  const url = date ? `/finance?date=${date}` : '/finance';
  const response = await api.get<FinanceSummary>(url);
  return response.data;
};
```

### Dashboard

#### Obter Resumo do Dashboard

**GET** `/api/dashboard/summary?date=YYYY-MM-DD`

**Query Parameters**:
- `date`: Data no formato YYYY-MM-DD (opcional, usa data atual se não fornecido)

**Response** (200 OK):
```json
{
  "active_students": 45,
  "today_classes": 3,
  "total_income_today": 300.00,
  "total_expense_today": 100.00
}
```

**Exemplo de Código**:
```typescript
// src/services/dashboardService.ts
import api from './api';

export interface DashboardSummary {
  active_students: number;
  today_classes: number;
  total_income_today: number;
  total_expense_today: number;
}

export const getDashboardSummary = async (date?: string): Promise<DashboardSummary> => {
  const url = date ? `/dashboard/summary?date=${date}` : '/dashboard/summary';
  const response = await api.get<DashboardSummary>(url);
  return response.data;
};
```

## ⚠️ Tratamento de Erros

### Estrutura de Erro

A API retorna erros no seguinte formato:

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Exemplo de Tratamento

```typescript
// src/utils/errorHandler.ts
import { AxiosError } from 'axios';

export const handleApiError = (error: unknown): string => {
  if (error instanceof AxiosError) {
    if (error.response) {
      // Erro com resposta do servidor
      const status = error.response.status;
      const detail = error.response.data?.detail || 'Erro desconhecido';
      
      switch (status) {
        case 400:
          return `Dados inválidos: ${detail}`;
        case 401:
          return 'Não autenticado. Faça login novamente.';
        case 404:
          return 'Recurso não encontrado.';
        case 500:
          return 'Erro no servidor. Tente novamente mais tarde.';
        default:
          return detail;
      }
    } else if (error.request) {
      // Requisição feita mas sem resposta
      return 'Erro de conexão. Verifique sua internet.';
    }
  }
  
  return 'Erro desconhecido. Tente novamente.';
};

// Uso em componentes React
import { useState } from 'react';
import { handleApiError } from './utils/errorHandler';

const MyComponent = () => {
  const [error, setError] = useState<string | null>(null);
  
  const fetchData = async () => {
    try {
      const data = await getStudents();
      // Processar dados
    } catch (err) {
      setError(handleApiError(err));
    }
  };
  
  return (
    <div>
      {error && <div className="error">{error}</div>}
      {/* ... */}
    </div>
  );
};
```

## 📊 Estruturas de Dados

### Tipos TypeScript Completos

```typescript
// src/types/api.ts

// Student
export interface Student {
  id: string;
  name: string;
  birthdate: string | null;
  phone: string | null;
  created_at: string;
}

export interface StudentCreate {
  name: string;
  birthdate?: string | null;
  phone?: string | null;
}

// Class
export interface Class {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

export interface ClassCreate {
  name: string;
  description?: string | null;
}

// Attendance
export interface Attendance {
  id: string;
  class_id: string;
  student_id: string;
  date_time: string;
  status: 'present' | 'absent';
}

export interface AttendanceCreate {
  class_id: string;
  student_id: string;
  status: 'present' | 'absent';
  date_time?: string;
}

// Evaluation
export interface Evaluation {
  id: string;
  student_id: string;
  date: string;
  weight_kg: number;
  height_m: number | null;
  measurements: Record<string, number> | null;
  notes: string | null;
  imc: number | null;
}

export interface EvaluationCreate {
  student_id: string;
  date: string;
  weight_kg: number;
  height_m?: number | null;
  measurements?: Record<string, number> | null;
  notes?: string | null;
}

export interface ChartData {
  labels: string[];
  weights: number[];
  imc: (number | null)[];
}

// Finance
export interface FinanceEntry {
  id: string;
  date_time: string;
  type: 'income' | 'expense';
  amount: number;
  payment_method: 'credit' | 'debit' | 'pix' | 'cash' | 'other';
  category: string | null;
  description: string | null;
  created_by: string | null;
}

export interface FinanceEntryCreate {
  type: 'income' | 'expense';
  amount: number;
  payment_method: 'credit' | 'debit' | 'pix' | 'cash' | 'other';
  category?: string | null;
  description?: string | null;
  date_time?: string;
}

export interface FinanceSummary {
  entries: FinanceEntry[];
  total_income: number;
  total_expense: number;
  balance: number;
}

// Dashboard
export interface DashboardSummary {
  active_students: number;
  today_classes: number;
  total_income_today: number;
  total_expense_today: number;
}
```

## ✅ Boas Práticas

### 1. Gerenciamento de Estado

Use React Query ou SWR para cache e sincronização automática:

```typescript
// Exemplo com React Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getStudents, createStudent } from './services/studentService';

// Listar alunos com cache
const useStudents = () => {
  return useQuery({
    queryKey: ['students'],
    queryFn: getStudents,
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

// Criar aluno com invalidação de cache
const useCreateStudent = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
    },
  });
};
```

### 2. Validação de Formulários

Use bibliotecas como React Hook Form + Zod:

```typescript
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const studentSchema = z.object({
  name: z.string().min(1, 'Nome é obrigatório'),
  birthdate: z.string().optional(),
  phone: z.string().optional(),
});

type StudentFormData = z.infer<typeof studentSchema>;

const StudentForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<StudentFormData>({
    resolver: zodResolver(studentSchema),
  });
  
  const onSubmit = async (data: StudentFormData) => {
    await createStudent(data);
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}
      {/* ... */}
    </form>
  );
};
```

### 3. Loading States

```typescript
const MyComponent = () => {
  const { data, isLoading, error } = useStudents();
  
  if (isLoading) return <div>Carregando...</div>;
  if (error) return <div>Erro ao carregar</div>;
  
  return (
    <div>
      {data?.map(student => (
        <div key={student.id}>{student.name}</div>
      ))}
    </div>
  );
};
```

### 4. Formatação de Datas

```typescript
// src/utils/dateUtils.ts
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('pt-BR');
};

export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};
```

## 📋 Checklist de Integração

### Configuração Inicial

- [ ] Configurar cliente HTTP (Axios ou Fetch)
- [ ] Configurar interceptors para autenticação
- [ ] Configurar tratamento de erros global
- [ ] Criar tipos TypeScript para todas as entidades
- [ ] Configurar variáveis de ambiente para URL da API

### Autenticação

- [ ] Implementar tela de login
- [ ] Armazenar token no localStorage
- [ ] Implementar logout
- [ ] Adicionar proteção de rotas (se necessário)

### Funcionalidades

- [ ] **Students**
  - [ ] Listar alunos
  - [ ] Criar aluno
  - [ ] Visualizar detalhes do aluno
  - [ ] Formulário de cadastro com validação

- [ ] **Classes**
  - [ ] Listar aulas
  - [ ] Criar aula
  - [ ] Formulário de cadastro

- [ ] **Attendance**
  - [ ] Registrar presença individual
  - [ ] Registrar presença em lote (bulk)
  - [ ] Listar presenças de uma aula
  - [ ] Filtro por data

- [ ] **Evaluations**
  - [ ] Criar avaliação
  - [ ] Listar avaliações de um aluno
  - [ ] Exibir gráfico de evolução (peso e IMC)
  - [ ] Integração com biblioteca de gráficos (Chart.js, Recharts, etc.)

- [ ] **Finance**
  - [ ] Criar lançamento financeiro
  - [ ] Visualizar fechamento de caixa
  - [ ] Exibir totais (receita, despesa, saldo)
  - [ ] Formatação de valores monetários

- [ ] **Dashboard**
  - [ ] Exibir resumo do dashboard
  - [ ] Cards com métricas principais
  - [ ] Filtro por data

### UX/UI

- [ ] Loading states em todas as requisições
- [ ] Mensagens de erro amigáveis
- [ ] Mensagens de sucesso após ações
- [ ] Validação de formulários
- [ ] Feedback visual para ações do usuário

### Testes

- [ ] Testar todos os endpoints
- [ ] Testar tratamento de erros
- [ ] Testar casos de borda (dados vazios, valores inválidos)
- [ ] Testar em diferentes navegadores

## 🔗 Recursos Adicionais

- **Documentação FastAPI**: https://fastapi.tiangolo.com/
- **Axios**: https://axios-http.com/
- **React Query**: https://tanstack.com/query/latest
- **React Hook Form**: https://react-hook-form.com/
- **Chart.js**: https://www.chartjs.org/
- **Recharts**: https://recharts.org/

## 📞 Suporte

Para dúvidas ou problemas na integração:

1. Consulte a documentação interativa em http://localhost:8000/docs
2. Verifique os logs do backend para erros detalhados
3. Teste os endpoints diretamente usando a documentação Swagger

---

**Última atualização**: Janeiro 2025
**Versão da API**: 1.0.0

