# AutoU Email Classifier - Backend

Backend em Python/Flask para classificação inteligente de emails usando IA.

## 🚀 Funcionalidades

- **Classificação Inteligente**: Classifica emails como "Produtivo" ou "Improdutivo"
- **Processamento de Arquivos**: Suporte para upload de arquivos TXT e PDF
- **IA Integrada**: Usa OpenAI GPT ou classificação baseada em regras
- **Respostas Automáticas**: Gera respostas contextuais para cada categoria
- **API RESTful**: Endpoints bem documentados para integração
- **Processamento em Lote**: Classifica múltiplos emails simultaneamente

## 🛠️ Tecnologias

- **Flask**: Framework web
- **OpenAI GPT**: Classificação e geração de respostas (opcional)
- **NLTK**: Processamento de linguagem natural
- **PyPDF2**: Extração de texto de PDFs
- **scikit-learn**: Algoritmos de machine learning
- **Flask-CORS**: Suporte a CORS para frontend

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Chave da API OpenAI (opcional, mas recomendado)

## 🔧 Instalação

1. **Clone o repositório e navegue para o backend:**
```bash
cd backend
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente:**
```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o arquivo .env e adicione sua chave da OpenAI (opcional)
OPENAI_API_KEY=sua_chave_aqui
```

## 🚀 Execução

1. **Inicie o servidor de desenvolvimento:**
```bash
python main.py
```

2. **A API estará disponível em:**
```
http://localhost:5000
```

3. **Teste a API:**
```bash
python test_api.py
```

## 📚 Endpoints da API

### Health Check
```http
GET /health
```
Verifica se a API está funcionando.

### Classificar Email
```http
POST /classify
```

**Corpo da requisição (texto):**
```json
{
  "text": "Olá, preciso de ajuda com o sistema..."
}
```

**Corpo da requisição (arquivo):**
```http
Content-Type: multipart/form-data
file: [arquivo.txt ou arquivo.pdf]
```

**Resposta:**
```json
{
  "original_text": "Olá, preciso de ajuda...",
  "category": "Produtivo",
  "suggested_response": "Obrigado por entrar em contato...",
  "confidence": 0.85
}
```

### Classificação em Lote
```http
POST /classify/batch
```

**Corpo da requisição:**
```json
{
  "emails": [
    "Email 1 aqui...",
    "Email 2 aqui...",
    "Email 3 aqui..."
  ]
}
```

## 🧪 Testes

Execute os testes automatizados:
```bash
python test_api.py
```

## 🔧 Configuração

### Variáveis de Ambiente

- `OPENAI_API_KEY`: Chave da API OpenAI (opcional)
- `FLASK_ENV`: Ambiente (development/production)
- `FLASK_DEBUG`: Modo debug (True/False)
- `MAX_CONTENT_LENGTH`: Tamanho máximo de upload (bytes)
- `CORS_ORIGINS`: Origens permitidas para CORS

### Classificação sem OpenAI

Se não configurar a chave da OpenAI, o sistema usará classificação baseada em regras que analisa:

- Palavras-chave específicas
- Presença de perguntas
- Indicadores de urgência
- Padrões de solicitação

## 🏗️ Arquitetura

```
backend/
├── main.py                 # Aplicação Flask principal
├── config.py              # Configurações
├── requirements.txt       # Dependências
├── test_api.py           # Testes da API
└── services/
    ├── __init__.py
    ├── email_processor.py    # Processamento de emails
    ├── ai_classifier.py      # Classificação com IA
    └── response_generator.py # Geração de respostas
```

## 🚀 Deploy

### Heroku
1. Instale o Heroku CLI
2. Crie um app: `heroku create seu-app-name`
3. Configure as variáveis: `heroku config:set OPENAI_API_KEY=sua_chave`
4. Deploy: `git push heroku main`

### Render
1. Conecte seu repositório
2. Configure as variáveis de ambiente
3. Deploy automático

### Railway
1. Conecte seu repositório
2. Configure as variáveis de ambiente
3. Deploy automático

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme se o Python 3.8+ está sendo usado
3. Teste a conectividade com `python test_api.py`
4. Verifique os logs para erros específicos

Para mais ajuda, abra uma issue no repositório.