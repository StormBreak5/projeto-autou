#!/usr/bin/env python3

import os
import sys
import subprocess
from setup_nltk import download_nltk_data

def check_dependencies():
    try:
        import flask
        import openai
        import nltk
        import PyPDF2
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def setup_environment():
    print("🔧 Configurando ambiente de desenvolvimento...")
    
    download_nltk_data()
    
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado")
        print("📋 Copiando .env.example para .env...")
        try:
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ Arquivo .env criado")
            print("ℹ️  Configure sua chave da OpenAI no arquivo .env para melhor performance")
        except FileNotFoundError:
            print("❌ Arquivo .env.example não encontrado")
    
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✅ Pasta {uploads_dir} criada")

def run_server():
    print("🚀 Iniciando servidor de desenvolvimento...")
    print("📍 API disponível em: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/health")
    print("📖 Para testar: python test_api.py")
    print("-" * 50)
    
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    
    from main import app
    app.run(debug=True, host='0.0.0.0', port=5000)

def main():
    print("🎯 AutoU Email Classifier - Servidor de Desenvolvimento")
    print("=" * 60)
    
    if not check_dependencies():
        sys.exit(1)
    
    setup_environment()
    
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n👋 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()