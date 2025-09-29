"""
Dados de treinamento para classificação de emails
Este arquivo contém exemplos de emails categorizados para treinar o modelo
"""

# Dados de exemplo para treinamento
TRAINING_DATA = [
    # Emails Produtivos
    {
        "email": "Prezados, gostaria de solicitar uma atualização sobre o status do meu processo de abertura de conta. O protocolo é #12345. Aguardo retorno.",
        "category": "Produtivo",
        "suggested_response": "Olá! Obrigado pelo contato. Verificamos que seu processo #12345 está em análise pela nossa equipe. Você receberá uma atualização em até 2 dias úteis. Qualquer dúvida, estamos à disposição."
    },
    {
        "email": "Bom dia, estou com dificuldades para acessar minha conta no sistema. Aparece erro 'usuário não encontrado'. Podem me ajudar?",
        "category": "Produtivo", 
        "suggested_response": "Bom dia! Lamentamos o inconveniente. Nossa equipe técnica irá verificar seu acesso e entrar em contato em até 24 horas para resolver a questão. Obrigado pela paciência."
    },
    {
        "email": "Preciso de esclarecimentos sobre as taxas cobradas na minha conta corrente. Podem me enviar um detalhamento?",
        "category": "Produtivo",
        "suggested_response": "Olá! Claro, vamos providenciar o detalhamento das taxas da sua conta. O documento será enviado para seu email cadastrado em até 1 dia útil. Agradecemos o contato."
    },
    {
        "email": "Solicito o cancelamento do meu cartão de crédito número final 1234. Como devo proceder?",
        "category": "Produtivo",
        "suggested_response": "Olá! Recebemos sua solicitação de cancelamento. Nossa equipe entrará em contato para confirmar os dados e processar o cancelamento de forma segura. Aguarde nosso retorno em até 48 horas."
    },
    {
        "email": "Gostaria de agendar uma reunião para discutir opções de investimento. Qual a disponibilidade da equipe?",
        "category": "Produtivo",
        "suggested_response": "Olá! Ficamos felizes com seu interesse em nossos produtos de investimento. Nossa equipe comercial entrará em contato para agendar uma reunião conforme sua disponibilidade. Obrigado!"
    },
    
    # Emails Improdutivos
    {
        "email": "Feliz Natal para toda a equipe! Desejo um 2024 cheio de prosperidade e sucesso!",
        "category": "Improdutivo",
        "suggested_response": "Muito obrigado pelas felicitações! Desejamos também um excelente ano novo para você e sua família. Continuamos à disposição para atendê-lo sempre que precisar."
    },
    {
        "email": "Parabéns pelo excelente atendimento que recebi ontem na agência. A funcionária Maria foi muito atenciosa.",
        "category": "Improdutivo",
        "suggested_response": "Ficamos muito felizes com seu feedback positivo! Vamos repassar seus elogios para a Maria e toda nossa equipe. Obrigado por escolher nossos serviços!"
    },
    {
        "email": "Obrigado pela resolução rápida do meu problema. Vocês são ótimos!",
        "category": "Improdutivo",
        "suggested_response": "Que bom saber que conseguimos ajudar! Seu feedback é muito importante para nós. Continuamos sempre à disposição para atendê-lo. Obrigado!"
    },
    {
        "email": "Boa tarde! Como está o clima aí hoje? Aqui está muito quente!",
        "category": "Improdutivo",
        "suggested_response": "Boa tarde! Obrigado pela mensagem. Caso precise de algum serviço bancário, estaremos sempre à disposição para atendê-lo. Tenha um ótimo dia!"
    },
    {
        "email": "Feliz aniversário para a empresa! 50 anos de tradição no mercado financeiro!",
        "category": "Improdutivo",
        "suggested_response": "Muito obrigado pelas felicitações! Ficamos honrados em ter clientes como você ao longo dessa jornada. Continuaremos trabalhando para oferecer sempre o melhor atendimento."
    }
]

# Dados adicionais para validação
VALIDATION_DATA = [
    {
        "email": "Preciso alterar meu endereço cadastrado. Como faço isso?",
        "category": "Produtivo",
        "suggested_response": "Olá! Para alterar seu endereço, você pode fazer isso pelo nosso app, internet banking ou comparecer a uma agência com documento de identidade e comprovante de residência atualizado."
    },
    {
        "email": "Muito obrigado pela ajuda de vocês. Problema resolvido!",
        "category": "Improdutivo", 
        "suggested_response": "Fico muito feliz em saber que conseguimos resolver! Sua satisfação é nossa prioridade. Qualquer coisa, estaremos sempre aqui para ajudar."
    }
]

def get_training_examples():
    """Retorna os dados de treinamento formatados"""
    return TRAINING_DATA

def get_validation_examples():
    """Retorna os dados de validação formatados"""
    return VALIDATION_DATA

def format_for_openai_training(data):
    """
    Formata os dados para o formato esperado pela OpenAI para fine-tuning
    """
    formatted_data = []
    
    for item in data:
        formatted_item = {
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em classificar emails bancários como 'Produtivo' (requer ação) ou 'Improdutivo' (não requer ação) e sugerir respostas apropriadas."
                },
                {
                    "role": "user", 
                    "content": f"Classifique este email e sugira uma resposta: {item['email']}"
                },
                {
                    "role": "assistant",
                    "content": f"Classificação: {item['category']}\nResposta sugerida: {item['suggested_response']}"
                }
            ]
        }
        formatted_data.append(formatted_item)
    
    return formatted_data