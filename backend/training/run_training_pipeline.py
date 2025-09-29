"""
Script automatizado para executar todo o pipeline de treinamento
"""

import os
import sys
import subprocess
import time
from datetime import datetime

# Adicionar o diretório pai ao path para importar load_env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load_env import load_env

# Carregar variáveis de ambiente
load_env()

class TrainingPipeline:
    def __init__(self):
        self.start_time = datetime.now()
        self.log_file = f"training_log_{self.start_time.strftime('%Y%m%d_%H%M%S')}.txt"
        
    def log(self, message):
        """Log com timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # Salvar no arquivo de log
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def check_prerequisites(self):
        """Verifica se todos os pré-requisitos estão atendidos"""
        self.log("Verificando pré-requisitos...")
        
        # Verificar API Key
        if not os.getenv('OPENAI_API_KEY'):
            self.log("ERRO: Variável OPENAI_API_KEY não configurada")
            return False
        
        # Verificar se os arquivos existem
        required_files = [
            'training_data.py',
            'fine_tune_model.py', 
            'evaluate_model.py',
            'data_augmentation.py'
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                self.log(f"ERRO: Arquivo {file} não encontrado")
                return False
        
        # Verificar dependências Python
        try:
            import openai
            self.log("✓ Biblioteca openai encontrada")
        except ImportError:
            self.log("ERRO: Biblioteca openai não instalada. Execute: pip install openai")
            return False
        
        self.log("✓ Todos os pré-requisitos atendidos")
        return True
    
    def run_data_augmentation(self, variations_per_email=2, num_synthetic=10):
        """Executa o aumento de dados"""
        self.log("Iniciando aumento de dados...")
        
        try:
            from data_augmentation import DataAugmenter
            
            augmenter = DataAugmenter()
            
            # Gerar variações
            self.log(f"Gerando {variations_per_email} variações por email...")
            augmented_data = augmenter.augment_training_data(variations_per_email)
            
            # Gerar emails sintéticos
            self.log(f"Criando {num_synthetic} emails sintéticos...")
            synthetic_data = augmenter.create_synthetic_emails(num_synthetic)
            
            # Combinar dados
            all_data = augmented_data + synthetic_data
            
            # Salvar
            filename = f"augmented_data_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            augmenter.save_augmented_data(all_data, filename)
            
            self.log(f"✓ Aumento de dados concluído. Total: {len(all_data)} exemplos")
            return filename
            
        except Exception as e:
            self.log(f"ERRO no aumento de dados: {e}")
            return None
    
    def run_fine_tuning(self):
        """Executa o fine-tuning do modelo"""
        self.log("Iniciando fine-tuning...")
        
        try:
            from fine_tune_model import EmailClassifierTrainer
            
            trainer = EmailClassifierTrainer()
            
            # Executar pipeline completo
            success = trainer.run_full_training_pipeline()
            
            if success and trainer.fine_tuned_model:
                self.log(f"✓ Fine-tuning concluído. Modelo: {trainer.fine_tuned_model}")
                return trainer.fine_tuned_model
            else:
                self.log("ERRO: Fine-tuning falhou")
                return None
                
        except Exception as e:
            self.log(f"ERRO no fine-tuning: {e}")
            return None
    
    def run_evaluation(self, model_id):
        """Executa a avaliação do modelo"""
        self.log(f"Iniciando avaliação do modelo {model_id}...")
        
        try:
            from evaluate_model import ModelEvaluator
            from training_data import get_validation_examples, get_training_examples
            
            evaluator = ModelEvaluator(model_id)
            
            # Avaliar com dados de validação
            validation_data = get_validation_examples()
            results = evaluator.evaluate_accuracy(validation_data)
            
            # Salvar resultados
            results_filename = f"evaluation_results_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            evaluator.save_evaluation_results(results, results_filename)
            
            # Log dos resultados principais
            self.log(f"✓ Avaliação concluída")
            self.log(f"  Acurácia: {results['accuracy']:.2%}")
            self.log(f"  Predições corretas: {results['correct_predictions']}/{results['total_predictions']}")
            
            return results
            
        except Exception as e:
            self.log(f"ERRO na avaliação: {e}")
            return None
    
    def run_full_pipeline(self, 
                         augment_data=True,
                         variations_per_email=2, 
                         num_synthetic=10,
                         run_fine_tune=True,
                         evaluate_model=True):
        """
        Executa o pipeline completo de treinamento
        """
        self.log("="*60)
        self.log("INICIANDO PIPELINE COMPLETO DE TREINAMENTO")
        self.log("="*60)
        
        # 1. Verificar pré-requisitos
        if not self.check_prerequisites():
            self.log("Pipeline interrompido devido a pré-requisitos não atendidos")
            return False
        
        # 2. Aumento de dados (opcional)
        augmented_file = None
        if augment_data:
            augmented_file = self.run_data_augmentation(variations_per_email, num_synthetic)
            if not augmented_file:
                self.log("AVISO: Aumento de dados falhou, continuando com dados originais")
        
        # 3. Fine-tuning (opcional)
        model_id = None
        if run_fine_tune:
            model_id = self.run_fine_tuning()
            if not model_id:
                self.log("ERRO: Fine-tuning falhou, não é possível continuar com avaliação")
                return False
        else:
            model_id = "gpt-3.5-turbo"  # Usar modelo padrão
            self.log("Pulando fine-tuning, usando modelo padrão")
        
        # 4. Avaliação (opcional)
        results = None
        if evaluate_model and model_id:
            results = self.run_evaluation(model_id)
        
        # 5. Resumo final
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        self.log("="*60)
        self.log("PIPELINE CONCLUÍDO")
        self.log("="*60)
        self.log(f"Tempo total: {duration}")
        self.log(f"Log salvo em: {self.log_file}")
        
        if augmented_file:
            self.log(f"Dados aumentados: {augmented_file}")
        
        if model_id and run_fine_tune:
            self.log(f"Modelo treinado: {model_id}")
        
        if results:
            self.log(f"Acurácia final: {results['accuracy']:.2%}")
        
        return True

def main():
    """
    Função principal com interface interativa
    """
    print("="*60)
    print("PIPELINE AUTOMATIZADO DE TREINAMENTO")
    print("="*60)
    
    pipeline = TrainingPipeline()
    
    # Configurações do pipeline
    print("\nConfiguração do Pipeline:")
    
    # Aumento de dados
    augment = input("Executar aumento de dados? (s/n) [s]: ").lower()
    augment_data = augment != 'n'
    
    variations_per_email = 2
    num_synthetic = 10
    
    if augment_data:
        try:
            variations_per_email = int(input("Variações por email [2]: ") or "2")
            num_synthetic = int(input("Emails sintéticos [10]: ") or "10")
        except ValueError:
            print("Usando valores padrão")
    
    # Fine-tuning
    fine_tune = input("Executar fine-tuning? (s/n) [s]: ").lower()
    run_fine_tune = fine_tune != 'n'
    
    # Avaliação
    evaluate = input("Executar avaliação? (s/n) [s]: ").lower()
    evaluate_model = evaluate != 'n'
    
    # Confirmação
    print(f"\nConfiguração:")
    print(f"- Aumento de dados: {'Sim' if augment_data else 'Não'}")
    if augment_data:
        print(f"  - Variações por email: {variations_per_email}")
        print(f"  - Emails sintéticos: {num_synthetic}")
    print(f"- Fine-tuning: {'Sim' if run_fine_tune else 'Não'}")
    print(f"- Avaliação: {'Sim' if evaluate_model else 'Não'}")
    
    confirm = input("\nIniciar pipeline? (s/n) [s]: ").lower()
    if confirm == 'n':
        print("Pipeline cancelado")
        return
    
    # Executar pipeline
    success = pipeline.run_full_pipeline(
        augment_data=augment_data,
        variations_per_email=variations_per_email,
        num_synthetic=num_synthetic,
        run_fine_tune=run_fine_tune,
        evaluate_model=evaluate_model
    )
    
    if success:
        print("\n✓ Pipeline executado com sucesso!")
    else:
        print("\n✗ Pipeline falhou. Verifique o log para detalhes.")

if __name__ == "__main__":
    main()