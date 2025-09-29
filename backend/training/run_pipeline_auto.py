#!/usr/bin/env python3
"""
Script para executar o pipeline de treinamento automaticamente com configurações padrão
"""

import sys
import os

# Adicionar o diretório pai ao path para importar load_env
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load_env import load_env

# Carregar variáveis de ambiente
load_env()

from run_training_pipeline import TrainingPipeline

def main():
    """
    Executa o pipeline com configurações padrão
    """
    print("="*60)
    print("EXECUTANDO PIPELINE COM CONFIGURAÇÕES PADRÃO")
    print("="*60)
    print("- Aumento de dados: Sim (2 variações por email, 10 sintéticos)")
    print("- Fine-tuning: Sim")
    print("- Avaliação: Sim")
    print("="*60)
    
    pipeline = TrainingPipeline()
    
    # Executar pipeline com configurações padrão
    success = pipeline.run_full_pipeline(
        augment_data=True,
        variations_per_email=2,
        num_synthetic=10,
        run_fine_tune=True,
        evaluate_model=True
    )
    
    if success:
        print("\n✓ Pipeline executado com sucesso!")
    else:
        print("\n✗ Pipeline falhou. Verifique o log para detalhes.")

if __name__ == "__main__":
    main()