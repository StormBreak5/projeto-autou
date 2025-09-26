#!/usr/bin/env python3

import nltk
import ssl

def download_nltk_data():
    try:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        print("📦 Baixando dados do NLTK...")
        
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        
        print("✅ Dados do NLTK baixados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao baixar dados do NLTK: {e}")
        print("ℹ️  O sistema funcionará com funcionalidade limitada")

if __name__ == "__main__":
    download_nltk_data()