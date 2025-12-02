# Guia de Deploy - Render

Este documento contém informações detalhadas sobre como fazer deploy da aplicação no Render.

## 📋 Checklist de Deploy

### Arquivos Necessários

- ✅ `requirements.txt` - Dependências do projeto
- ✅ `render.yaml` - Configuração do Render (opcional, mas recomendado)
- ✅ `app/main.py` - Aplicação FastAPI configurada para produção

### Variáveis de Ambiente

Configure as seguintes variáveis no dashboard do Render:

| Variável | Valor Padrão | Descrição | Obrigatório |
|----------|--------------|-----------|-------------|
| `ENVIRONMENT` | `development` | Ambiente de execução (`development` ou `production`) | Não |
| `PORT` | - | **NÃO CONFIGURE MANUALMENTE** - Render define automaticamente | Não |
| `ALLOWED_ORIGINS` | `*` | URLs permitidas para CORS (separadas por vírgula) | Não (mas recomendado em produção) |

⚠️ **IMPORTANTE**: Nunca configure a variável `PORT` manualmente no Render. O Render define essa variável automaticamente para serviços web. Se você configurar manualmente, pode causar erros de deploy.

### Exemplo de Configuração para Produção

```env
ENVIRONMENT=production
ALLOWED_ORIGINS=https://meu-frontend.com,https://www.meu-frontend.com
```

## 🚀 Processo de Deploy

### Opção 1: Deploy Manual

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório Git
4. Configure:
   - **Name**: `academia-be`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Adicione variáveis de ambiente (se necessário)
6. Clique em "Create Web Service"

### Opção 2: Deploy com render.yaml (Recomendado)

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em "New +" → "Blueprint"
3. Conecte seu repositório Git
4. O Render detectará automaticamente o `render.yaml`
5. Revise as configurações e clique em "Apply"
6. Configure variáveis de ambiente no dashboard após o deploy

## ⚙️ Configurações do render.yaml

O arquivo `render.yaml` já está configurado com:

- **Runtime**: Python 3.11.0
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`
- **Plan**: Free (pode ser alterado)

## 🔍 Verificação Pós-Deploy

Após o deploy, verifique:

1. **Health Check**: `https://seu-app.onrender.com/health`
   - Deve retornar: `{"status": "healthy"}`

2. **Documentação**: `https://seu-app.onrender.com/docs`
   - Deve abrir a documentação Swagger

3. **API Root**: `https://seu-app.onrender.com/`
   - Deve retornar informações da API

## ⚠️ Limitações Importantes

### Armazenamento de Dados

⚠️ **ATENÇÃO**: Este projeto usa arquivos JSON como banco de dados. No Render:

- Os dados são armazenados no sistema de arquivos **efêmero**
- Os dados serão **perdidos** quando:
  - O serviço reiniciar
  - O serviço for atualizado/redeployado
  - O serviço ficar inativo (no plano Free)

### Recomendações

Para produção, considere migrar para:

- **PostgreSQL** (Render oferece banco de dados PostgreSQL)
- **MongoDB Atlas** (serviço gerenciado)
- **Supabase** (PostgreSQL + Auth)

## 🔧 Troubleshooting

### Erro: "Invalid value for '--port': '...' is not a valid integer"

**Causa**: A variável `PORT` está configurada manualmente no dashboard do Render com um valor inválido.

**Solução**: 
1. Acesse o dashboard do Render
2. Vá em "Environment" no seu serviço
3. **Remova** a variável `PORT` se ela estiver configurada manualmente
4. O Render define `PORT` automaticamente - não precisa configurar manualmente
5. Faça um novo deploy

### Erro: "Module not found"

**Solução**: Verifique se todas as dependências estão no `requirements.txt`

### Erro: "Port already in use"

**Solução**: Certifique-se de usar `$PORT` no startCommand, não um número fixo

### Erro: "CORS blocked"

**Solução**: Configure `ALLOWED_ORIGINS` com as URLs corretas do frontend

### Dados não persistem

**Solução**: Isso é esperado com arquivos JSON. Migre para um banco de dados persistente.

## 📚 Recursos Adicionais

- [Documentação do Render](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-fastapi)
- [Render Environment Variables](https://render.com/docs/environment-variables)

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs no dashboard do Render
2. Confirme que todas as variáveis de ambiente estão configuradas
3. Teste localmente antes de fazer deploy
4. Consulte a documentação do Render

