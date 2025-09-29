# Treinamento e Fine-tuning do Modelo de Classificação de Emails

Este diretório contém scripts para treinar, avaliar e melhorar o modelo de IA usado para classificar emails bancários.

## Arquivos Disponíveis

### 1. `training_data.py`
Contém os dados de treinamento e validação para o modelo.
- **Dados de treinamento**: Exemplos de emails categorizados como "Produtivo" ou "Improdutivo"
- **Dados de validação**: Conjunto separado para testar a performance
- **Funções de formatação**: Prepara dados no formato esperado pela OpenAI

### 2. `fine_tune_model.py`
Script principal para fazer fine-tuning do modelo OpenAI.

**Funcionalidades:**
- Preparação de arquivos de treinamento no formato JSONL
- Upload de dados para OpenAI
- Criação e monitoramento de jobs de fine-tuning
- Teste do modelo treinado

**Como usar:**
```bash
cd backend/training
python fine_tune_model.py
```

### 3. `evaluate_model.py`
Avalia a performance do modelo treinado.

**Métricas calculadas:**
- Acurácia geral
- Matriz de confusão
- Precisão, Recall e F1-Score
- Análise detalhada de erros

**Como usar:**
```bash
cd backend/training
python evaluate_model.py
```

### 4. `data_augmentation.py`
Aumenta o conjunto de dados de treinamento.

**Funcionalidades:**
- Gera variações dos emails existentes
- Cria emails sintéticos completamente novos
- Gera respostas apropriadas automaticamente

**Como usar:**
```bash
cd backend/training
python data_augmentation.py
```

## Pré-requisitos

1. **Variável de ambiente OPENAI_API_KEY**:
   ```bash
   # Windows
   set OPENAI_API_KEY=sua_chave_aqui
   
   # Linux/Mac
   export OPENAI_API_KEY=sua_chave_aqui
   ```

2. **Dependências Python**:
   ```bash
   pip install openai
   ```

## Fluxo de Trabalho Recomendado

### 1. Preparação dos Dados
```bash
# Aumentar dados de treinamento (opcional)
python data_augmentation.py
```

### 2. Fine-tuning do Modelo
```bash
# Treinar modelo personalizado
python fine_tune_model.py
```

### 3. Avaliação
```bash
# Avaliar performance do modelo
python evaluate_model.py
```

## Estrutura dos Dados de Treinamento

Cada exemplo de treinamento contém:
```python
{
    "email": "Texto do email do cliente",
    "category": "Produtivo" ou "Improdutivo", 
    "suggested_response": "Resposta sugerida para o email"
}
```

## Categorias de Classificação

### Produtivo
Emails que requerem uma ação ou resposta específica:
- Solicitações de suporte técnico
- Pedidos de informações sobre conta
- Problemas que precisam ser resolvidos
- Dúvidas sobre produtos/serviços

### Improdutivo  
Emails que não necessitam de ação imediata:
- Mensagens de agradecimento
- Felicitações e cortesias
- Elogios ao atendimento
- Comentários gerais positivos

## Custos da OpenAI

**Fine-tuning (gpt-3.5-turbo)**:
- Treinamento: ~$0.008 por 1K tokens
- Uso do modelo: ~$0.012 por 1K tokens (input) + $0.016 por 1K tokens (output)

**Estimativa para este projeto**:
- Dados base (~15 exemplos): ~$0.50-1.00
- Com aumento de dados (~50 exemplos): ~$2.00-4.00

## Dicas de Otimização

1. **Qualidade dos Dados**: Prefira qualidade à quantidade
2. **Balanceamento**: Mantenha proporção similar entre categorias
3. **Validação**: Sempre teste com dados não vistos durante o treinamento
4. **Iteração**: Refine os dados baseado nos resultados da avaliação

## Monitoramento

O script `fine_tune_model.py` monitora automaticamente o progresso do treinamento e exibe:
- Status atual do job
- Tempo estimado de conclusão
- ID do modelo final

## Troubleshooting

### Erro de API Key
```
Erro: Configure a variável de ambiente OPENAI_API_KEY
```
**Solução**: Configure a chave da API OpenAI nas variáveis de ambiente.

### Erro de Quota
```
You exceeded your current quota
```
**Solução**: Verifique os limites da sua conta OpenAI ou adicione créditos.

### Erro de Formato
```
Invalid file format
```
**Solução**: Verifique se o arquivo JSONL está no formato correto.

## Próximos Passos

1. **Coleta de Dados Reais**: Substitua os dados sintéticos por emails reais (anonimizados)
2. **Feedback Loop**: Implemente sistema para coletar feedback dos usuários
3. **Retreinamento**: Configure retreinamento periódico com novos dados
4. **A/B Testing**: Compare performance entre diferentes versões do modelo