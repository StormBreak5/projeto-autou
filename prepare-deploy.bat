@echo off
echo 🚀 Preparando projeto para deploy na Vercel...

REM Verificar se estamos no diretório correto
if not exist "vercel.json" (
    echo ❌ Erro: Execute este script no diretório raiz do projeto
    exit /b 1
)

echo 📦 Instalando dependências do frontend...
cd frontend
call npm install

echo 🔨 Testando build de produção...
call npm run build:prod

if %errorlevel% neq 0 (
    echo ❌ Erro no build de produção
    exit /b 1
)

cd ..

echo 🔍 Verificando estrutura do projeto...
echo ✅ vercel.json encontrado
echo ✅ api/index.py encontrado
echo ✅ frontend/dist criado

echo.
echo 🎉 Projeto pronto para deploy!
echo.
echo Próximos passos:
echo 1. Faça commit e push para seu repositório Git
echo 2. Acesse vercel.com e conecte seu repositório
echo 3. Configure as variáveis de ambiente:
echo    - OPENAI_API_KEY: sua chave da OpenAI
echo    - FLASK_ENV: production
echo 4. Faça o deploy!
echo.
echo 📖 Veja o guia completo em DEPLOY_VERCEL.md

pause