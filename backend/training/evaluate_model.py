"""
Script para avaliar a performance do modelo treinado
"""

import json
import os
import sys
from openai import OpenAI
from training_data import get_validation_examples, get_training_examples
import re
from collections import Counter

# Adicionar o diretório pai ao path para importar load_env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load_env import load_env

# Carregar variáveis de ambiente
load_env()

class ModelEvaluator:
    def __init__(self, model_id=None):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model_id = model_id or "gpt-3.5-turbo"  # Modelo padrão se não especificado
        
    def extract_classification(self, response_text):
        """
        Extrai a classificação da resposta do modelo
        """
        # Procura por padrões como "Classificação: Produtivo" ou "Categoria: Improdutivo"
        patterns = [
            r"Classificação:\s*(Produtivo|Improdutivo)",
            r"Categoria:\s*(Produtivo|Improdutivo)", 
            r"Tipo:\s*(Produtivo|Improdutivo)",
            r"(Produtivo|Improdutivo)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        
        return "Não identificado"
    
    def classify_email(self, email_text):
        """
        Classifica um email usando o modelo
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente especializado em classificar emails bancários como 'Produtivo' (requer ação) ou 'Improdutivo' (não requer ação) e sugerir respostas apropriadas."
                    },
                    {
                        "role": "user",
                        "content": f"Classifique este email e sugira uma resposta: {email_text}"
                    }
                ],
                temperature=0.1  # Baixa temperatura para respostas mais consistentes
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro ao classificar email: {e}")
            return None
    
    def evaluate_accuracy(self, test_data):
        """
        Avalia a acurácia do modelo nos dados de teste
        """
        correct_predictions = 0
        total_predictions = 0
        detailed_results = []
        
        print("=== Avaliando Modelo ===")
        
        for i, item in enumerate(test_data):
            email = item['email']
            expected_category = item['category']
            
            print(f"\nTestando email {i+1}/{len(test_data)}...")
            
            # Classificar email
            response = self.classify_email(email)
            
            if response:
                predicted_category = self.extract_classification(response)
                
                # Verificar se a predição está correta
                is_correct = predicted_category.lower() == expected_category.lower()
                
                if is_correct:
                    correct_predictions += 1
                
                total_predictions += 1
                
                # Armazenar resultado detalhado
                result = {
                    'email': email[:100] + "..." if len(email) > 100 else email,
                    'expected': expected_category,
                    'predicted': predicted_category,
                    'correct': is_correct,
                    'full_response': response
                }
                detailed_results.append(result)
                
                print(f"Esperado: {expected_category} | Predito: {predicted_category} | {'✓' if is_correct else '✗'}")
            
            else:
                print("Erro na classificação")
        
        # Calcular métricas
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        return {
            'accuracy': accuracy,
            'correct_predictions': correct_predictions,
            'total_predictions': total_predictions,
            'detailed_results': detailed_results
        }
    
    def generate_confusion_matrix(self, results):
        """
        Gera uma matriz de confusão simples
        """
        true_positives = 0  # Produtivo classificado como Produtivo
        true_negatives = 0  # Improdutivo classificado como Improdutivo
        false_positives = 0  # Improdutivo classificado como Produtivo
        false_negatives = 0  # Produtivo classificado como Improdutivo
        
        for result in results['detailed_results']:
            expected = result['expected'].lower()
            predicted = result['predicted'].lower()
            
            if expected == 'produtivo' and predicted == 'produtivo':
                true_positives += 1
            elif expected == 'improdutivo' and predicted == 'improdutivo':
                true_negatives += 1
            elif expected == 'improdutivo' and predicted == 'produtivo':
                false_positives += 1
            elif expected == 'produtivo' and predicted == 'improdutivo':
                false_negatives += 1
        
        return {
            'true_positives': true_positives,
            'true_negatives': true_negatives,
            'false_positives': false_positives,
            'false_negatives': false_negatives
        }
    
    def print_evaluation_report(self, results):
        """
        Imprime um relatório detalhado da avaliação
        """
        print("\n" + "="*50)
        print("RELATÓRIO DE AVALIAÇÃO DO MODELO")
        print("="*50)
        
        print(f"\nACURÁCIA GERAL: {results['accuracy']:.2%}")
        print(f"Predições corretas: {results['correct_predictions']}/{results['total_predictions']}")
        
        # Matriz de confusão
        confusion = self.generate_confusion_matrix(results)
        print(f"\nMATRIZ DE CONFUSÃO:")
        print(f"Verdadeiros Positivos (Produtivo → Produtivo): {confusion['true_positives']}")
        print(f"Verdadeiros Negativos (Improdutivo → Improdutivo): {confusion['true_negatives']}")
        print(f"Falsos Positivos (Improdutivo → Produtivo): {confusion['false_positives']}")
        print(f"Falsos Negativos (Produtivo → Improdutivo): {confusion['false_negatives']}")
        
        # Calcular precisão e recall
        precision = confusion['true_positives'] / (confusion['true_positives'] + confusion['false_positives']) if (confusion['true_positives'] + confusion['false_positives']) > 0 else 0
        recall = confusion['true_positives'] / (confusion['true_positives'] + confusion['false_negatives']) if (confusion['true_positives'] + confusion['false_negatives']) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\nMÉTRICAS DETALHADAS:")
        print(f"Precisão: {precision:.2%}")
        print(f"Recall: {recall:.2%}")
        print(f"F1-Score: {f1_score:.2%}")
        
        # Erros mais comuns
        print(f"\nERROS ENCONTRADOS:")
        for result in results['detailed_results']:
            if not result['correct']:
                print(f"- Email: {result['email']}")
                print(f"  Esperado: {result['expected']} | Predito: {result['predicted']}")
                print()
    
    def save_evaluation_results(self, results, filename='evaluation_results.json'):
        """
        Salva os resultados da avaliação em um arquivo JSON
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"Resultados salvos em: {filename}")

def main():
    """
    Função principal para executar a avaliação
    """
    # Verificar se a API key está configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("Erro: Configure a variável de ambiente OPENAI_API_KEY")
        return
    
    print("=== AVALIADOR DE MODELO DE CLASSIFICAÇÃO DE EMAILS ===")
    
    # Solicitar ID do modelo (opcional)
    model_id = input("Digite o ID do modelo fine-tuned (ou pressione Enter para usar gpt-3.5-turbo): ").strip()
    
    if not model_id:
        model_id = "gpt-3.5-turbo"
        print("Usando modelo padrão: gpt-3.5-turbo")
    
    # Criar avaliador
    evaluator = ModelEvaluator(model_id)
    
    # Escolher dados de teste
    print("\nEscolha os dados para avaliação:")
    print("1. Dados de validação")
    print("2. Dados de treinamento")
    print("3. Ambos")
    
    choice = input("Digite sua escolha (1-3): ")
    
    test_data = []
    if choice == "1":
        test_data = get_validation_examples()
    elif choice == "2":
        test_data = get_training_examples()
    elif choice == "3":
        test_data = get_validation_examples() + get_training_examples()
    else:
        print("Opção inválida!")
        return
    
    # Executar avaliação
    results = evaluator.evaluate_accuracy(test_data)
    
    # Mostrar relatório
    evaluator.print_evaluation_report(results)
    
    # Salvar resultados
    save_results = input("\nDeseja salvar os resultados? (s/n): ").lower()
    if save_results == 's':
        evaluator.save_evaluation_results(results)

if __name__ == "__main__":
    main()