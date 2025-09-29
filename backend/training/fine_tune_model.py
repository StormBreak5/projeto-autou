"""
Script para fine-tuning do modelo OpenAI para classificação de emails
"""

import json
import os
import sys
from openai import OpenAI
from training_data import get_training_examples, format_for_openai_training
import time

# Adicionar o diretório pai ao path para importar load_env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load_env import load_env

# Carregar variáveis de ambiente
load_env()

class EmailClassifierTrainer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.training_file_id = None
        self.fine_tuned_model = None
        
    def prepare_training_file(self, output_file='training_data.jsonl'):
        """
        Prepara o arquivo de treinamento no formato JSONL para OpenAI
        """
        training_data = get_training_examples()
        formatted_data = format_for_openai_training(training_data)
        
        # Salva no formato JSONL
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in formatted_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"Arquivo de treinamento criado: {output_file}")
        return output_file
    
    def upload_training_file(self, file_path):
        """
        Faz upload do arquivo de treinamento para OpenAI
        """
        try:
            with open(file_path, 'rb') as f:
                response = self.client.files.create(
                    file=f,
                    purpose='fine-tune'
                )
            
            self.training_file_id = response.id
            print(f"Arquivo enviado com sucesso. ID: {self.training_file_id}")
            return self.training_file_id
            
        except Exception as e:
            print(f"Erro ao enviar arquivo: {e}")
            return None
    
    def create_fine_tune_job(self, model="gpt-3.5-turbo"):
        """
        Cria um job de fine-tuning
        """
        if not self.training_file_id:
            print("Erro: Arquivo de treinamento não foi enviado")
            return None
            
        try:
            response = self.client.fine_tuning.jobs.create(
                training_file=self.training_file_id,
                model=model,
                hyperparameters={
                    "n_epochs": 3,  # Número de épocas de treinamento
                }
            )
            
            job_id = response.id
            print(f"Job de fine-tuning criado: {job_id}")
            return job_id
            
        except Exception as e:
            print(f"Erro ao criar job de fine-tuning: {e}")
            return None
    
    def monitor_fine_tune_job(self, job_id):
        """
        Monitora o progresso do job de fine-tuning
        """
        print("Monitorando progresso do fine-tuning...")
        
        while True:
            try:
                job = self.client.fine_tuning.jobs.retrieve(job_id)
                status = job.status
                
                print(f"Status atual: {status}")
                
                if status == "succeeded":
                    self.fine_tuned_model = job.fine_tuned_model
                    print(f"Fine-tuning concluído! Modelo: {self.fine_tuned_model}")
                    return self.fine_tuned_model
                    
                elif status == "failed":
                    print("Fine-tuning falhou!")
                    return None
                    
                elif status in ["running", "queued"]:
                    print("Aguardando conclusão...")
                    time.sleep(30)  # Aguarda 30 segundos antes de verificar novamente
                    
            except Exception as e:
                print(f"Erro ao monitorar job: {e}")
                time.sleep(30)
    
    def test_fine_tuned_model(self, test_email):
        """
        Testa o modelo fine-tuned com um email de exemplo
        """
        if not self.fine_tuned_model:
            print("Erro: Modelo fine-tuned não disponível")
            return None
            
        try:
            response = self.client.chat.completions.create(
                model=self.fine_tuned_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente especializado em classificar emails bancários como 'Produtivo' (requer ação) ou 'Improdutivo' (não requer ação) e sugerir respostas apropriadas."
                    },
                    {
                        "role": "user",
                        "content": f"Classifique este email e sugira uma resposta: {test_email}"
                    }
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro ao testar modelo: {e}")
            return None
    
    def run_full_training_pipeline(self):
        """
        Executa todo o pipeline de treinamento
        """
        print("=== Iniciando Pipeline de Fine-tuning ===")
        
        # 1. Preparar arquivo de treinamento
        training_file = self.prepare_training_file()
        
        # 2. Upload do arquivo
        file_id = self.upload_training_file(training_file)
        if not file_id:
            return False
        
        # 3. Criar job de fine-tuning
        job_id = self.create_fine_tune_job()
        if not job_id:
            return False
        
        # 4. Monitorar progresso
        model_id = self.monitor_fine_tune_job(job_id)
        if not model_id:
            return False
        
        # 5. Testar modelo
        test_email = "Gostaria de saber o saldo da minha conta corrente."
        result = self.test_fine_tuned_model(test_email)
        
        if result:
            print(f"\n=== Teste do Modelo ===")
            print(f"Email de teste: {test_email}")
            print(f"Resposta do modelo: {result}")
        
        print(f"\n=== Fine-tuning Concluído ===")
        print(f"Modelo ID: {model_id}")
        
        return True

def main():
    """
    Função principal para executar o treinamento
    """
    # Verificar se a API key está configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("Erro: Configure a variável de ambiente OPENAI_API_KEY")
        return
    
    trainer = EmailClassifierTrainer()
    
    # Opção 1: Executar pipeline completo
    print("Escolha uma opção:")
    print("1. Executar pipeline completo de fine-tuning")
    print("2. Apenas preparar arquivo de treinamento")
    print("3. Testar modelo existente")
    
    choice = input("Digite sua escolha (1-3): ")
    
    if choice == "1":
        trainer.run_full_training_pipeline()
        
    elif choice == "2":
        trainer.prepare_training_file()
        print("Arquivo de treinamento preparado com sucesso!")
        
    elif choice == "3":
        model_id = input("Digite o ID do modelo fine-tuned: ")
        trainer.fine_tuned_model = model_id
        
        test_email = input("Digite o email para testar: ")
        result = trainer.test_fine_tuned_model(test_email)
        
        if result:
            print(f"Resultado: {result}")
        
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()