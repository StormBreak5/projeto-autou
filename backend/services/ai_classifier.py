import os
import openai
import logging
from typing import Tuple
import json

logger = logging.getLogger(__name__)

class AIClassifier:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.last_confidence = 0.0
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.use_openai = True
            logger.info("Usando OpenAI para classificação")
        else:
            self.use_openai = False
            logger.info("OpenAI não configurado, usando classificação baseada em regras")
    
    def classify(self, text: str) -> str:
        try:
            if self.use_openai:
                return self._classify_with_openai(text)
            else:
                return self._classify_with_rules(text)
        except Exception as e:
            logger.error(f"Erro na classificação: {str(e)}")
            return self._classify_with_rules(text)
    
    def _classify_with_openai(self, text: str) -> str:
        try:
            prompt = self._build_classification_prompt(text)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip()
            
            if "produtivo" in result.lower():
                classification = "Produtivo"
                self.last_confidence = 0.85
            else:
                classification = "Improdutivo"
                self.last_confidence = 0.85
            
            return classification
            
        except Exception as e:
            logger.error(f"Erro na classificação OpenAI: {str(e)}")
            raise
    
    def _classify_with_rules(self, text: str) -> str:
        text_lower = text.lower()
        
        productive_keywords = [
            'suporte', 'técnico', 'problema', 'erro', 'bug', 'falha',
            'solicitação', 'pedido', 'requisição', 'dúvida', 'questão',
            'status', 'atualização', 'andamento', 'prazo', 'urgente',
            'sistema', 'aplicação', 'funcionalidade', 'recurso',
            'configuração', 'instalação', 'acesso', 'login', 'senha',
            'relatório', 'dados', 'informação', 'documento', 'arquivo'
        ]
        
        unproductive_keywords = [
            'parabéns', 'felicitações', 'aniversário', 'natal', 'ano novo',
            'feriado', 'férias', 'obrigado', 'agradecimento', 'grato',
            'bom dia', 'boa tarde', 'boa noite', 'cumprimento',
            'convite', 'evento', 'festa', 'reunião social', 'coffee'
        ]
        
        productive_score = sum(1 for keyword in productive_keywords if keyword in text_lower)
        unproductive_score = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
        
        has_question = '?' in text
        has_request_words = any(word in text_lower for word in ['preciso', 'gostaria', 'poderia', 'favor', 'solicito'])
        has_problem_indicators = any(word in text_lower for word in ['não funciona', 'erro', 'problema', 'falha'])
        
        if has_question or has_request_words or has_problem_indicators:
            productive_score += 2
        
        if productive_score > unproductive_score:
            self.last_confidence = min(0.9, 0.6 + (productive_score - unproductive_score) * 0.1)
            return "Produtivo"
        else:
            self.last_confidence = min(0.9, 0.6 + (unproductive_score - productive_score) * 0.1)
            return "Improdutivo"
    
    def _build_classification_prompt(self, text: str) -> str:
        return f"""
        Classifique o seguinte email como "Produtivo" ou "Improdutivo":

        Email: "{text}"

        Critérios:
        - Produtivo: Emails que requerem ação ou resposta específica (suporte técnico, dúvidas sobre sistema, solicitações, atualizações de status)
        - Improdutivo: Emails que não necessitam ação imediata (felicitações, agradecimentos, mensagens sociais)

        Responda apenas com "Produtivo" ou "Improdutivo".
        """
    
    def _get_system_prompt(self) -> str:
        return """
        Você é um assistente especializado em classificar emails corporativos.
        Sua tarefa é determinar se um email é "Produtivo" (requer ação) ou "Improdutivo" (não requer ação imediata).
        Seja preciso e consistente em suas classificações.
        """
    
    def get_last_confidence(self) -> float:
        return self.last_confidence