# 🚀 Guia de Deploy - AutoU Email Classifier Backend

Este guia contém instruções para fazer deploy da API em diferentes plataformas de nuvem.

## 📋 Pré-requisitos

- Conta na plataforma escolhida
- Repositório Git com o código
- Chave da API OpenAI (opcional, mas recomendado)

## 🌐 Opções de Deploy

### 1. Render (Recomendado - Gratuito)

**Vantagens:** Gratuito, fácil configuração, SSL automático

1. **Acesse [render.com](https://render.com) e faça login**

2. **Crie um novo Web Service:**
   - Conecte seu repositório GitHub
   - Selecione a pasta `backend`
   - Configure:
     - **Build Command:** `pip install -r requirements.txt && python setup_nltk.py`
     - **Start Command:** `python main.py`
     - **Environment:** Python 3

3. **Configure as variáveis de ambiente:**
   ```
   OPENAI_API_KEY=sua_chave_aqui
   FLASK_ENV=production
   PORT=10000
   ```

4. **Deploy automático será iniciado**

### 2. Railway

**Vantagens:** Deploy simples, boa performance

1. **Acesse [railway.app](https://railway.app) e faça login**

2. **Crie um novo projeto:**
   - Conecte seu repositório
   - Railway detectará automaticamente que é Python

3. **Configure variáveis de ambiente:**
   ```
   OPENAI_API_KEY=sua_chave_aqui
   FLASK_ENV=production
   ```

4. **Deploy automático**

### 3. Heroku

**Vantagens:** Tradicional, muitos recursos

1. **Instale o Heroku CLI**

2. **Faça login e crie app:**
   ```bash
   heroku login
   heroku create seu-app-name
   ```

3. **Configure variáveis:**
   ```bash
   heroku config:set OPENAI_API_KEY=sua_chave
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

### 4. Vercel

**Vantagens:** Rápido, boa integração com frontend

1. **Instale Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Configure vercel.json na raiz do backend:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

### 5. Google Cloud Platform (GCP)

**Vantagens:** Escalável, integração com outros serviços Google

1. **Instale Google Cloud SDK**

2. **Configure projeto:**
   ```bash
   gcloud init
   gcloud app create
   ```

3. **Crie app.yaml:**
   ```yaml
   runtime: python311
   
   env_variables:
     OPENAI_API_KEY: "sua_chave_aqui"
     FLASK_ENV: "production"
   
   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

4. **Deploy:**
   ```bash
   gcloud app deploy
   ```

### 6. AWS (Elastic Beanstalk)

**Vantagens:** Robusto, muitos recursos AWS

1. **Instale EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Inicialize:**
   ```bash
   eb init
   eb create production
   ```

3. **Configure variáveis:**
   ```bash
   eb setenv OPENAI_API_KEY=sua_chave FLASK_ENV=production
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

## 🔧 Configurações Importantes

### Variáveis de Ambiente Obrigatórias

```bash
# Produção
FLASK_ENV=production

# OpenAI (opcional mas recomendado)
OPENAI_API_KEY=sua_chave_da_openai

# CORS (ajuste conforme seu frontend)
CORS_ORIGINS=https://seu-frontend.com,https://outro-dominio.com
```

### Configurações de Performance

Para produção, considere:

1. **Usar Gunicorn** (adicione ao requirements.txt):
   ```
   gunicorn==21.2.0
   ```

2. **Atualizar Procfile:**
   ```
   web: gunicorn --bind 0.0.0.0:$PORT main:app
   ```

3. **Configurar workers:**
   ```bash
   # Para Heroku/Railway
   web: gunicorn --workers 2 --bind 0.0.0.0:$PORT main:app
   ```

## 🧪 Testando o Deploy

Após o deploy, teste sua API:

1. **Health Check:**
   ```bash
   curl https://sua-api.com/health
   ```

2. **Classificação:**
   ```bash
   curl -X POST https://sua-api.com/classify \
     -H "Content-Type: application/json" \
     -d '{"text": "Preciso de ajuda com o sistema"}'
   ```

## 🔍 Monitoramento

### Logs
- **Render:** Dashboard > Logs
- **Railway:** Dashboard > Deployments > Logs  
- **Heroku:** `heroku logs --tail`
- **Vercel:** Dashboard > Functions > Logs

### Métricas
- Configure alertas para:
  - Tempo de resposta > 5s
  - Taxa de erro > 5%
  - Uso de memória > 80%

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de dependências:**
   ```bash
   # Verifique se requirements.txt está correto
   pip freeze > requirements.txt
   ```

2. **Erro de NLTK:**
   ```bash
   # Certifique-se que setup_nltk.py está sendo executado
   python setup_nltk.py
   ```

3. **Erro de CORS:**
   ```bash
   # Configure CORS_ORIGINS corretamente
   export CORS_ORIGINS=https://seu-frontend.com
   ```

4. **Timeout:**
   ```bash
   # Aumente timeout se usando OpenAI
   # Configure workers do Gunicorn
   ```

### Logs Úteis

```python
# Adicione logs para debug
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Classificando email: {email_text[:50]}...")
logger.error(f"Erro na classificação: {str(e)}")
```

## 📊 Performance

### Otimizações Recomendadas

1. **Cache de modelos:** Carregue modelos uma vez na inicialização
2. **Pool de conexões:** Para APIs externas
3. **Compressão:** Habilite gzip
4. **CDN:** Para arquivos estáticos

### Limites Típicos

- **Render (Free):** 512MB RAM, sleep após inatividade
- **Railway (Free):** 512MB RAM, 500h/mês
- **Heroku (Free):** Descontinuado
- **Vercel:** 1024MB RAM, 10s timeout

## 🔐 Segurança

1. **HTTPS:** Sempre use HTTPS em produção
2. **Rate Limiting:** Implemente para evitar abuso
3. **Validação:** Valide todos os inputs
4. **Secrets:** Nunca commite chaves no código

## 📈 Escalabilidade

Para alto volume:

1. **Load Balancer:** Distribua carga
2. **Cache Redis:** Para respostas frequentes
3. **Queue System:** Para processamento assíncrono
4. **Database:** Para histórico e analytics

## 🎯 Próximos Passos

Após deploy bem-sucedido:

1. Configure monitoramento
2. Implemente analytics
3. Adicione testes automatizados
4. Configure CI/CD
5. Documente API com Swagger

---

**Dica:** Comece com Render ou Railway para prototipagem rápida, depois migre para AWS/GCP conforme necessário.