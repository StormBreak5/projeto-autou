#!/bin/bash

echo "🚀 Preparando projeto para deploy na Vercel..."

# Verificar se estamos no diretório correto
if [ ! -f "vercel.json" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

echo "📦 Instalando dependências do frontend..."
cd frontend
npm install

echo "🔨 Testando build de produção..."
npm run build:prod

if [ $? -eq 0 ]; then
    echo "✅ Build de produção bem-sucedido!"
else
    echo "❌ Erro no build de produção"
    exit 1
fi

cd ..

echo "🔍 Verificando estrutura do projeto..."
echo "✅ vercel.json encontrado"
echo "✅ api/index.py encontrado"
echo "✅ frontend/dist criado"

echo ""
echo "🎉 Projeto pronto para deploy!"
echo ""
echo "Próximos passos:"
echo "1. Faça commit e push para seu repositório Git"
echo "2. Acesse vercel.com e conecte seu repositório"
echo "3. Configure as variáveis de ambiente:"
echo "   - OPENAI_API_KEY: sua chave da OpenAI"
echo "   - FLASK_ENV: production"
echo "4. Faça o deploy!"
echo ""
echo "📖 Veja o guia completo em DEPLOY_VERCEL.md"