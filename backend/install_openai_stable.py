#!/usr/bin/env python3

import subprocess
import sys

def install_stable_openai():
    print("🔧 Instalando versão estável da OpenAI")
    print("=" * 50)
    
    commands = [
        "pip uninstall openai -y",
        "pip uninstall openai-api -y", 
        "pip cache purge",
        "pip install openai==0.28.1"  # Versão estável mais antiga
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}️⃣ Executando: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ Sucesso")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Aviso: {e}")
    
    # Teste
    print("5️⃣ Testando importação...")
    try:
        import openai
        print(f"✅ OpenAI versão: {openai.__version__}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if install_stable_openai():
        print("\n🎉 Instalação concluída!")
        print("Execute: python run_dev.py")
    else:
        print("\n❌ Falha na instalação")