#!/usr/bin/env python3

import requests
import json

API_BASE_URL = "http://localhost:5000"

def test_health():
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_classify_text():
    print("\n🔍 Testando classificação de texto...")
    
    test_emails = [
        {
            "text": "Olá, estou com um problema no sistema. O login não está funcionando e preciso acessar urgentemente. Podem me ajudar?",
            "expected": "Produtivo"
        },
        {
            "text": "Boa tarde! Gostaria de parabenizar toda a equipe pelo excelente trabalho. Muito obrigado por tudo!",
            "expected": "Improdutivo"
        },
        {
            "text": "Preciso do relatório mensal de vendas. Quando estará disponível? É para uma apresentação importante.",
            "expected": "Produtivo"
        },
        {
            "text": "Feliz Natal para toda a equipe! Que 2024 seja um ano repleto de sucessos!",
            "expected": "Improdutivo"
        }
    ]
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n--- Teste {i} ---")
        print(f"Email: {email['text'][:50]}...")
        print(f"Esperado: {email['expected']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/classify",
                json={"text": email["text"]},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Classificação: {result['category']}")
                print(f"Confiança: {result.get('confidence', 'N/A')}")
                print(f"Resposta sugerida: {result['suggested_response'][:100]}...")
                
                if result['category'] == email['expected']:
                    print("✅ Classificação correta!")
                else:
                    print("❌ Classificação incorreta!")
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

def test_batch_classify():
    print("\n🔍 Testando classificação em lote...")
    
    emails = [
        "Preciso de suporte técnico urgente!",
        "Obrigado pela ajuda de ontem!",
        "Qual o status do meu pedido?",
        "Feliz aniversário!"
    ]
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/classify/batch",
            json={"emails": emails},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Processados {len(result['results'])} emails:")
            
            for i, res in enumerate(result['results']):
                if 'error' not in res:
                    print(f"  {i+1}. {res['category']} (confiança: {res.get('confidence', 'N/A')})")
                else:
                    print(f"  {i+1}. Erro: {res['error']}")
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    print("🚀 Iniciando testes da API AutoU Email Classifier")
    print("=" * 50)
    
    if not test_health():
        print("❌ API não está respondendo. Verifique se o servidor está rodando.")
        return
    
    test_classify_text()
    test_batch_classify()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    main()