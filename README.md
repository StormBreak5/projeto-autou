# AutoU - Classificador Inteligente de Emails

Sistema de classificação automática de emails usando Inteligência Artificial para identificar emails produtivos e improdutivos, gerando respostas automáticas contextuais.

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte do processo seletivo da AutoU, simulando uma solução real para automatizar a triagem de emails corporativos. O sistema utiliza IA para:

- **Classificar emails** em "Produtivo" (requer ação) ou "Improdutivo" (não requer ação imediata)
- **Gerar respostas automáticas** adequadas para cada categoria
- **Processar arquivos** de texto (.txt) e PDF (.pdf)
- **Fornecer interface intuitiva** para usuários não técnicos

## 🏗️ Arquitetura do Sistema

```
projeto-autou/
├── backend/                 # API Python (Flask + IA)
│   ├── main.py             # Aplicação principal
│   ├── services/           # Serviços especializados
│   │   ├── email_processor.py    # Processamento de emails
│   │   ├── ai_classifier.py      # Classificação com IA
│   │   └── response_generator.py # Geração de respostas
│   ├── requirements.txt    # Dependências Python
│   └── run_dev.py         # Script de desenvolvimento
└── frontend/               # Interface Angular + Material Design
    ├── src/app/           # Componentes da aplicação
    ├── package.json       # Dependências Node.js
    └── angular.json       # Configuração Angular
```

## 🚀 Instalação Local

### Pré-requisitos

- **Python 3.8+** (recomendado: 3.11)
- **Node.js 16+** e npm
- **Git** para clonar o repositório

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/projeto-autou.git
cd projeto-autou
```

### 2. Configuração do Backend

```bash
# Navegue para a pasta do backend
cd backend

# Crie um ambiente virtual Python
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente (opcional)
copy .env.example .env
# Edite o arquivo .env e adicione sua chave da OpenAI se tiver uma

# Execute o servidor de desenvolvimento
python run_dev.py
```

O backend estará disponível em: **http://localhost:5000**

### 3. Configuração do Frontend

```bash
# Em um novo terminal, navegue para a pasta do frontend
cd frontend

# Instale as dependências do Node.js
npm install

# Execute o servidor de desenvolvimento
ng serve
```

O frontend estará disponível em: **http://localhost:4200**

### 4. Verificação da Instalação

1. Acesse **http://localhost:4200** no seu navegador
2. Você deve ver a interface do AutoU Email Classifier
3. Teste a API acessando **http://localhost:5000/health**

## 📱 Como Usar a Aplicação

### Para Usuários Finais

#### 1. Acessando o Sistema
- Abra seu navegador e acesse a URL da aplicação
- A interface principal será exibida com o título "AutoU - Classificador de Emails"

#### 2. Classificando um Email

**Opção A: Digitando o Texto**
1. Selecione "Digitar texto" na seção "Método de entrada"
2. Cole ou digite o conteúdo do email na caixa de texto
3. Clique em "Classificar Email"
4. Aguarde o processamento (1-3 segundos)

**Opção B: Upload de Arquivo**
1. Selecione "Upload arquivo" na seção "Método de entrada"
2. Clique em "Selecionar arquivo" e escolha um arquivo .txt ou .pdf
3. Visualize o preview do conteúdo
4. Clique em "Classificar Email"

#### 3. Interpretando os Resultados

**Classificação:**
- 🟢 **Produtivo**: Email requer ação ou resposta (ex: suporte técnico, dúvidas, solicitações)
- 🟡 **Improdutivo**: Email não requer ação imediata (ex: agradecimentos, felicitações)

**Confiança:**
- Barra de progresso mostra a certeza da classificação (65% - 95%)
- Maior confiança = classificação mais precisa

**Resposta Sugerida:**
- Texto de resposta automática adequado à categoria
- Clique no ícone de cópia para copiar a resposta
- Use como base para sua resposta real

#### 4. Exemplos Práticos

**Email Produtivo:**
```
"Olá, estou com problema no sistema de login. 
Não consigo acessar minha conta há 2 horas. 
Podem me ajudar urgentemente?"
```
→ Resultado: Produtivo (85% confiança)
→ Resposta: "Recebemos sua solicitação de suporte técnico..."

**Email Improdutivo:**
```
"Boa tarde! Gostaria de parabenizar toda a equipe 
pelo excelente trabalho na apresentação de ontem. 
Muito obrigado!"
```
→ Resultado: Improdutivo (92% confiança)
→ Resposta: "Muito obrigado pelas felicitações!..."

### Para Desenvolvedores

#### Testando a API

```bash
# Teste básico da API
cd backend
python test_api.py

# Teste manual com curl
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Preciso de ajuda com o sistema"}'
```

#### Endpoints Disponíveis

- `GET /health` - Verificação de saúde da API
- `POST /classify` - Classificação de email individual
- `POST /classify/batch` - Classificação em lote

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` no backend com:

```env
# Chave da OpenAI (opcional, melhora a precisão)
OPENAI_API_KEY=sua_chave_aqui

# Configurações do Flask
FLASK_ENV=development
FLASK_DEBUG=True

# CORS (ajuste conforme necessário)
CORS_ORIGINS=http://localhost:4200
```

### Melhorando a Precisão

1. **Com OpenAI**: Configure sua chave da API para usar GPT-3.5
2. **Sem OpenAI**: O sistema usa classificação baseada em regras (funciona bem)

## 🚀 Deploy em Produção

### Opções Recomendadas

1. **Render** (Gratuito)
2. **Railway** (Gratuito)
3. **Vercel** (Frontend) + **Heroku** (Backend)

Consulte `backend/DEPLOYMENT.md` para instruções detalhadas.

## 🧪 Testes

```bash
# Backend
cd backend
python test_api.py

# Frontend
cd frontend
npm test
```

## 📊 Tecnologias Utilizadas

**Backend:**
- Python 3.11 + Flask
- OpenAI GPT-3.5 (opcional)
- NLTK para processamento de texto
- PyPDF2 para leitura de PDFs

**Frontend:**
- Angular 17 + TypeScript
- Angular Material Design
- RxJS para programação reativa

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido para o processo seletivo da AutoU.

## 🆘 Suporte

### Problemas Comuns

**Backend não inicia:**
- Verifique se o Python 3.8+ está instalado
- Confirme que o ambiente virtual está ativo
- Execute `pip install -r requirements.txt` novamente

**Frontend não carrega:**
- Verifique se o Node.js 16+ está instalado
- Execute `npm install` novamente
- Confirme que o backend está rodando

**Erro de CORS:**
- Verifique se o backend está rodando na porta 5000
- Confirme as configurações de CORS no arquivo `.env`

### Contato

Para dúvidas sobre este projeto, abra uma issue no repositório ou entre em contato através do processo seletivo da AutoU.

---

**Desenvolvido com ❤️ para a AutoU** - Automatizando o futuro do atendimento por email
