"""
Script para aumentar os dados de treinamento usando variações automáticas
"""

import os
import json
import sys
from openai import OpenAI
from training_data import get_training_examples
import random

# Adicionar o diretório pai ao path para importar load_env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load_env import load_env

# Carregar variáveis de ambiente
load_env()

class DataAugmenter:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_variations(self, original_email, category, num_variations=3):
        """
        Gera variações de um email mantendo a mesma categoria
        """
        prompt = f"""
        Gere {num_variations} variações do seguinte email, mantendo o mesmo sentido e categoria ({category}), mas mudando as palavras e estrutura:

        Email original: "{original_email}"
        Categoria: {category}

        As variações devem:
        1. Manter o mesmo propósito e categoria
        2. Usar vocabulário diferente
        3. Ter estruturas de frase variadas
        4. Ser realistas para o contexto bancário

        Formato de resposta:
        Variação 1: [texto]
        Variação 2: [texto]
        Variação 3: [texto]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em comunicação bancária que cria variações realistas de emails de clientes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8  # Maior criatividade para variações
            )
            
            return self.parse_variations(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Erro ao gerar variações: {e}")
            return []
    
    def parse_variations(self, response_text):
        """
        Extrai as variações do texto de resposta
        """
        variations = []
        lines = response_text.split('\n')
        
        for line in lines:
            if line.strip().startswith('Variação'):
                # Extrair o texto após os dois pontos
                if ':' in line:
                    variation = line.split(':', 1)[1].strip()
                    if variation:
                        variations.append(variation)
        
        return variations
    
    def generate_response_for_email(self, email_text, category):
        """
        Gera uma resposta apropriada para um email
        """
        prompt = f"""
        Gere uma resposta profissional e apropriada para este email de cliente bancário:

        Email: "{email_text}"
        Categoria: {category}

        A resposta deve ser:
        - Profissional e cortês
        - Apropriada para um banco
        - Específica para a categoria ({category})
        - Concisa mas completa

        Resposta:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um atendente bancário experiente que escreve respostas profissionais para emails de clientes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            return None
    
    def augment_training_data(self, variations_per_email=2):
        """
        Aumenta os dados de treinamento gerando variações
        """
        original_data = get_training_examples()
        augmented_data = []
        
        print(f"Gerando variações para {len(original_data)} emails originais...")
        
        for i, item in enumerate(original_data):
            print(f"Processando email {i+1}/{len(original_data)}...")
            
            # Adicionar email original
            augmented_data.append(item)
            
            # Gerar variações
            variations = self.generate_variations(
                item['email'], 
                item['category'], 
                variations_per_email
            )
            
            # Criar entradas para cada variação
            for variation in variations:
                # Gerar resposta para a variação
                suggested_response = self.generate_response_for_email(
                    variation, 
                    item['category']
                )
                
                if suggested_response:
                    augmented_item = {
                        'email': variation,
                        'category': item['category'],
                        'suggested_response': suggested_response,
                        'is_variation': True,
                        'original_index': i
                    }
                    augmented_data.append(augmented_item)
        
        print(f"Dados aumentados: {len(original_data)} → {len(augmented_data)} emails")
        return augmented_data
    
    def create_synthetic_emails(self, num_emails=10):
        """
        Cria emails sintéticos completamente novos
        """
        categories = ['Produtivo', 'Improdutivo']
        synthetic_emails = []
        
        for category in categories:
            emails_per_category = num_emails // 2
            
            if category == 'Produtivo':
                prompt = f"""
                Crie {emails_per_category} emails DIFERENTES de clientes bancários que requerem uma ação ou resposta específica (categoria Produtiva).

                Exemplos de temas:
                - Solicitações de informações sobre conta
                - Problemas técnicos
                - Pedidos de alteração de dados
                - Dúvidas sobre produtos
                - Reclamações que precisam de resolução

                Formato:
                Email 1: [texto do email]
                Email 2: [texto do email]
                ...
                """
            else:
                prompt = f"""
                Crie {emails_per_category} emails DIFERENTES de clientes bancários que NÃO requerem ação imediata (categoria Improdutiva).

                Exemplos de temas:
                - Agradecimentos
                - Felicitações
                - Elogios ao atendimento
                - Mensagens de cortesia
                - Comentários gerais positivos

                Formato:
                Email 1: [texto do email]
                Email 2: [texto do email]
                ...
                """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "Você é um especialista em comunicação bancária que cria emails realistas de clientes."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.9
                )
                
                # Extrair emails da resposta
                emails = self.parse_synthetic_emails(response.choices[0].message.content)
                
                # Gerar respostas para cada email
                for email in emails:
                    suggested_response = self.generate_response_for_email(email, category)
                    
                    if suggested_response:
                        synthetic_item = {
                            'email': email,
                            'category': category,
                            'suggested_response': suggested_response,
                            'is_synthetic': True
                        }
                        synthetic_emails.append(synthetic_item)
                
            except Exception as e:
                print(f"Erro ao criar emails sintéticos para {category}: {e}")
        
        return synthetic_emails
    
    def parse_synthetic_emails(self, response_text):
        """
        Extrai emails sintéticos do texto de resposta
        """
        emails = []
        lines = response_text.split('\n')
        
        for line in lines:
            if line.strip().startswith('Email'):
                if ':' in line:
                    email = line.split(':', 1)[1].strip()
                    if email and len(email) > 10:  # Filtrar emails muito curtos
                        emails.append(email)
        
        return emails
    
    def save_augmented_data(self, data, filename='augmented_training_data.json'):
        """
        Salva os dados aumentados em um arquivo
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Dados aumentados salvos em: {filename}")
        
        # Estatísticas
        original_count = len([item for item in data if not item.get('is_variation', False) and not item.get('is_synthetic', False)])
        variation_count = len([item for item in data if item.get('is_variation', False)])
        synthetic_count = len([item for item in data if item.get('is_synthetic', False)])
        
        print(f"\nEstatísticas:")
        print(f"Emails originais: {original_count}")
        print(f"Variações geradas: {variation_count}")
        print(f"Emails sintéticos: {synthetic_count}")
        print(f"Total: {len(data)}")

def main():
    """
    Função principal para executar o aumento de dados
    """
    if not os.getenv('OPENAI_API_KEY'):
        print("Erro: Configure a variável de ambiente OPENAI_API_KEY")
        return
    
    augmenter = DataAugmenter()
    
    print("=== AUMENTO DE DADOS DE TREINAMENTO ===")
    print("1. Gerar variações dos dados existentes")
    print("2. Criar emails sintéticos")
    print("3. Ambos")
    
    choice = input("Digite sua escolha (1-3): ")
    
    all_data = []
    
    if choice in ["1", "3"]:
        print("\nGerando variações dos dados existentes...")
        variations_per_email = int(input("Quantas variações por email? (recomendado: 2-3): ") or "2")
        augmented_data = augmenter.augment_training_data(variations_per_email)
        all_data.extend(augmented_data)
    
    if choice in ["2", "3"]:
        print("\nCriando emails sintéticos...")
        num_synthetic = int(input("Quantos emails sintéticos criar? (recomendado: 10-20): ") or "10")
        synthetic_data = augmenter.create_synthetic_emails(num_synthetic)
        all_data.extend(synthetic_data)
    
    if choice == "1":
        all_data = augmented_data
    elif choice == "2":
        all_data = synthetic_data
    
    # Salvar dados
    if all_data:
        augmenter.save_augmented_data(all_data)
        print("\nAumento de dados concluído com sucesso!")
    else:
        print("Nenhum dado foi gerado.")

if __name__ == "__main__":
    main()