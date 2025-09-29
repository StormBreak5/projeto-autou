#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

def test_openai_connection():
    print("🔍 Testando conexão com OpenAI...")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar se a chave existe
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
        return False
    
    print(f"✅ Chave encontrada: {api_key[:10]}...{api_key[-10:]}")
    
    # Testar importação do openai
    try:
        import openai
        print("✅ Biblioteca openai importada com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar openai: {e}")
        print("Execute: pip install openai")
        return False
    
    print("✅ Preparando cliente OpenAI")
    
    # Testar conexão real
    try:
        print("🔄 Testando conexão real com OpenAI...")
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de teste."},
                {"role": "user", "content": "Responda apenas 'OK' se você recebeu esta mensagem."}
            ],
            max_tokens=10,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Resposta da OpenAI: '{result}'")
        print("✅ Conexão com OpenAI funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com OpenAI: {e}")
        print(f"Tipo do erro: {type(e).__name__}")
        
        if "invalid_api_key" in str(e).lower():
            print("💡 Dica: Verifique se sua chave da API está correta")
        elif "quota" in str(e).lower():
            print("💡 Dica: Você pode ter excedido sua cota gratuita")
        elif "billing" in str(e).lower():
            print("💡 Dica: Pode ser necessário configurar billing na OpenAI")
        
        return False

def test_classifier_service():
    print("\n🔍 Testando serviço de classificação...")
    print("=" * 50)
    
    try:
        from services.ai_classifier import AIClassifier
        
        classifier = AIClassifier()
        print(f"✅ AIClassifier criado")
        print(f"📊 Usando OpenAI: {classifier.use_openai}")
        
        if classifier.use_openai:
            print("🔄 Testando classificação com OpenAI...")
            result = classifier.classify("Preciso de ajuda com um problema técnico urgente")
            print(f"✅ Resultado: {result}")
            print(f"📈 Confiança: {classifier.get_last_confidence()}")
        else:
            print("⚠️  Classificador está usando regras, não OpenAI")
            
    except Exception as e:
        print(f"❌ Erro no serviço de classificação: {e}")
        return False
    
    return True

def main():
    print("🚀 Diagnóstico da Integração OpenAI")
    print("=" * 60)
    
    # Teste 1: Conexão direta
    openai_ok = test_openai_connection()
    
    # Teste 2: Serviço de classificação
    classifier_ok = test_classifier_service()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    print(f"🔗 Conexão OpenAI: {'✅ OK' if openai_ok else '❌ FALHOU'}")
    print(f"🤖 Serviço Classificação: {'✅ OK' if classifier_ok else '❌ FALHOU'}")
    
    if openai_ok and classifier_ok:
        print("\n🎉 Tudo funcionando! OpenAI está integrada corretamente.")
    else:
        print("\n🔧 Há problemas que precisam ser resolvidos.")
        print("\n💡 PRÓXIMOS PASSOS:")
        if not openai_ok:
            print("1. Verifique sua chave da OpenAI")
            print("2. Confirme que tem créditos disponíveis")
            print("3. Teste a chave no site da OpenAI")
        if not classifier_ok:
            print("4. Reinicie o servidor backend")
            print("5. Verifique os logs do servidor")

if __name__ == "__main__":
    main()