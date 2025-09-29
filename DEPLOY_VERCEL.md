# 🚀 Deploy na Vercel - Guia Completo

## 📋 Pré-requisitos

1. **Conta na Vercel**: [vercel.com](https://vercel.com)
2. **Repositório Git**: Projeto deve estar no GitHub, GitLab ou Bitbucket
3. **Chave OpenAI**: Para o funcionamento da IA

## 🔧 Preparação do Projeto

### 1. Estrutura Configurada ✅

O projeto já está configurado com:
- `vercel.json` - Configuração de deploy
- `api/index.py` - Backend como Vercel Function
- `package.json` - Scripts de build
- Environment de produção configurado

### 2. Arquivos Criados

```
projeto-autou/
├── vercel.json              # Configuração Vercel
├── package.json             # Scripts de build
├── api/
│   ├── index.py            # Backend como Function
│   └── requirements.txt    # Dependências Python
├── frontend/               # App Angular
└── backend/               # Código fonte backend
```

## 🚀 Processo de Deploy

### Opção 1: Deploy via Dashboard Vercel (Recomendado)

1. **Acesse** [vercel.com/dashboard](https://vercel.com/dashboard)

2. **Clique em "New Project"**

3. **Conecte seu repositório Git**
   - Selecione GitHub/GitLab/Bitbucket
   - Escolha o repositório do projeto

4. **Configure o projeto**
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: npm run build
   Output Directory: frontend/dist/frontend
   Install Command: npm run install-frontend
   ```

5. **Adicione variáveis de ambiente**
   - `OPENAI_API_KEY`: Sua chave da OpenAI
   - `FLASK_ENV`: production

6. **Clique em "Deploy"**

### Opção 2: Deploy via CLI

1. **Instale a Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Faça login**
   ```bash
   vercel login
   ```

3. **Deploy do projeto**
   ```bash
   vercel --prod
   ```

4. **Configure variáveis de ambiente**
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add FLASK_ENV
   ```

## ⚙️ Configuração de Variáveis de Ambiente

### No Dashboard Vercel:
1. Vá em **Settings > Environment Variables**
2. Adicione:
   - **OPENAI_API_KEY**: `sk-...` (sua chave OpenAI)
   - **FLASK_ENV**: `production`

### Via CLI:
```bash
vercel env add OPENAI_API_KEY production
# Cole sua chave quando solicitado

vercel env add FLASK_ENV production
# Digite: production
```

## 🔍 Verificação do Deploy

### URLs de Teste:
- **Frontend**: `https://seu-projeto.vercel.app`
- **API Health**: `https://seu-projeto.vercel.app/api/health`
- **API Classify**: `https://seu-projeto.vercel.app/api/classify`

### Teste da API:
```bash
curl -X POST https://seu-projeto.vercel.app/api/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Preciso de ajuda com meu cartão"}'
```

## 🐛 Troubleshooting

### Problemas Comuns:

1. **Build falha no frontend**
   ```bash
   # Teste local primeiro
   cd frontend
   npm install
   npm run build:prod
   ```

2. **API não funciona**
   - Verifique se `OPENAI_API_KEY` está configurada
   - Veja logs em Vercel Dashboard > Functions

3. **CORS errors**
   - Já configurado para aceitar todas as origens
   - Verifique se as rotas estão corretas

4. **Timeout na API**
   - Configurado para 30s máximo
   - Para processos longos, considere otimização

### Logs e Debug:
- **Dashboard**: Vercel > Seu Projeto > Functions > View Logs
- **CLI**: `vercel logs`

## 🔄 Atualizações

### Deploy automático:
- Conecte o repositório Git
- Cada push na branch main fará deploy automático

### Deploy manual:
```bash
vercel --prod
```

## 📊 Monitoramento

### Métricas disponíveis:
- **Analytics**: Tráfego e performance
- **Functions**: Execuções e erros
- **Speed Insights**: Performance do frontend

## 🎯 Otimizações Recomendadas

1. **Cache**: Configurar cache headers
2. **CDN**: Vercel CDN automático
3. **Compression**: Gzip automático
4. **Edge Functions**: Para melhor performance global

## 🔐 Segurança

- ✅ HTTPS automático
- ✅ Variáveis de ambiente seguras
- ✅ CORS configurado
- ✅ Rate limiting (Vercel automático)

## 💰 Custos

### Plano Hobby (Gratuito):
- 100GB bandwidth/mês
- 100 execuções serverless/dia
- Domínios .vercel.app

### Plano Pro ($20/mês):
- Bandwidth ilimitado
- 1000 execuções serverless/dia
- Domínios customizados

---

## ✅ Checklist Final

- [ ] Repositório no Git
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Frontend carregando
- [ ] API respondendo
- [ ] Teste de classificação funcionando

**🎉 Seu projeto está no ar!**

URL: `https://seu-projeto.vercel.app`