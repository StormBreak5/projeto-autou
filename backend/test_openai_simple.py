#!/usr/bin/env python3

import os
from dotenv import load_dotenv

def test_openai_simple():
    print("🔍 Teste Simples da OpenAI")
    print("=" * 40)
    
    # Carregar .env
    load_dotenv()
    
    # Verificar chave
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Chave não encontrada no .env")
        return
    
    print(f"✅ Chave encontrada: {api_key[:15]}...")
    
    # Testar importação
    try:
        from openai import OpenAI
        print("✅ Biblioteca importada")
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return
    
    # Testar cliente
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Cliente criado")
    except Exception as e:
        print(f"❌ Erro ao criar cliente: {e}")
        return
    
    # Testar API
    try:
        print("🔄 Testando API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Diga apenas 'OK'"}],
            max_tokens=5
        )
        
        result = response.choices[0].message.content
        print(f"✅ Resposta: {result}")
        print("🎉 OpenAI funcionando!")
        
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        print(f"Tipo: {type(e).__name__}")

if __name__ == "__main__":
    test_openai_simple()