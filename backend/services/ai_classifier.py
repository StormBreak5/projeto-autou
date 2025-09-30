import os
import logging
from typing import Tuple
import json
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AIClassifier:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.last_confidence = 0.0
        self.client = None
        self.use_openai = False
        # Evite hardcode de IDs inexistentes em produção; use GPT-4o-mini como fallback leve
        self.custom_model = os.getenv('OPENAI_CUSTOM_MODEL', 'gpt-4o-mini')
        
        if self.openai_api_key and self.openai_api_key != 'your_openai_api_key_here':
            try:
                import openai
                import httpx
                
                if hasattr(openai, 'OpenAI'):
                    self.client = openai.OpenAI(
                        api_key=self.openai_api_key,
                        http_client=httpx.Client(timeout=15)
                    )
                else:
                    openai.api_key = self.openai_api_key
                    self.client = openai
                
                self.use_openai = True
                logger.info("Usando OpenAI para classificação")
            except Exception as e:
                logger.error(f"Erro ao inicializar OpenAI: {str(e)}")
                logger.info("Fallback para classificação baseada em regras")
                self.use_openai = False
        else:
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
            
            if hasattr(self.client, 'chat') and hasattr(self.client.chat, 'completions'):
                response = self.client.chat.completions.create(
                    model=self.custom_model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.0
                )
                result = response.choices[0].message.content.strip()
            else:
                # Legacy SDK
                response = self.client.ChatCompletion.create(
                    model=self.custom_model,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.0
                )
                result = response.choices[0].message.content.strip()
            
            classification, confidence = self._parse_openai_response(result, text)
            self.last_confidence = confidence
            
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
        return f"Classifique este email e sugira uma resposta: {text}"
    
    def _get_system_prompt(self) -> str:
        return "Você é um assistente especializado em classificar emails bancários como Produtivo (requer ação) ou Improdutivo (não requer ação) e sugerir respostas apropriadas."
    
    def _parse_openai_response(self, response_text: str, email_text: str = "") -> Tuple[str, float]:
        try:
            import json
            
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            response_data = json.loads(response_text)
            
            classificacao = response_data.get('classificacao', '').strip()
            confianca = float(response_data.get('confianca', 0.8))
            
            if 'improdutivo' in classificacao.lower():
                classification = "Improdutivo"
            elif 'produtivo' in classificacao.lower():
                classification = "Produtivo"
            else:
                justificativa = response_data.get('justificativa', '').lower()
                if any(word in justificativa for word in ['produtivo', 'ação', 'resposta', 'suporte']):
                    classification = "Produtivo"
                else:
                    classification = "Improdutivo"
            
            confianca = max(0.1, min(1.0, confianca))
            
            logger.info(f"OpenAI classificou como: {classification} (confiança: {confianca:.2f})")
            return classification, confianca
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.info(f"Modelo personalizado retornou: {response_text[:100]}...")
            
            response_lines = response_text.strip().split('\n')
            first_line = response_lines[0] if response_lines else response_text
            
            if 'classificação:' in first_line.lower():
                classification_part = first_line.lower().split('classificação:')[1].strip()
                if 'improdutivo' in classification_part:
                    classification = "Improdutivo"
                elif 'produtivo' in classification_part:
                    classification = "Produtivo"
                else:
                    classification = self._fallback_classification(response_text)
            else:
                response_lower = response_text.lower()
                
                if ('classificação: improdutivo' in response_lower or 
                    'classificacao: improdutivo' in response_lower or
                    'email improdutivo' in response_lower or
                    'improdutivo.' in response_lower):
                    classification = "Improdutivo"
                elif ('classificação: produtivo' in response_lower or 
                      'classificacao: produtivo' in response_lower or
                      'email produtivo' in response_lower or
                      'produtivo.' in response_lower):
                    classification = "Produtivo"
                else:
                    classification = self._fallback_classification(response_text)
            
            confidence = self._calculate_confidence_for_custom_model(classification, email_text)
            confidence = max(0.1, min(1.0, confidence))
            
            logger.info(f"Modelo personalizado classificou como: {classification} (confiança calculada: {confidence:.2f})")
            return classification, confidence

    def _fallback_classification(self, response_text: str) -> str:
        response_lower = response_text.lower()
        
        strong_unproductive = [
            'obrigado', 'agradecemos', 'felizes', 'parabéns', 'reconhecimento',
            'feedback positivo', 'elogios', 'satisfação', 'gratidão', 'felicitações'
        ]
        
        strong_productive = [
            'verificar', 'analisar', 'resolver', 'providenciar', 'processar',
            'encaminhar', 'agendar', 'solicitar', 'atualização', 'protocolo'
        ]
        
        unproductive_phrases = [
            'ficamos felizes', 'muito obrigado', 'feedback é importante',
            'continuamos à disposição', 'agradecemos o contato',
            'como posso ajudar', 'olá!', 'bom dia!', 'boa tarde!'
        ]
        
        productive_phrases = [
            'vamos verificar', 'nossa equipe', 'entrar em contato',
            'providenciar', 'em até', 'dias úteis', 'processar',
            'para resolver', 'vamos analisar'
        ]
        
        unproductive_score = 0
        productive_score = 0
        
        for indicator in strong_unproductive:
            if indicator in response_lower:
                unproductive_score += 2
        
        for indicator in strong_productive:
            if indicator in response_lower:
                productive_score += 2
                
        for phrase in unproductive_phrases:
            if phrase in response_lower:
                unproductive_score += 3
                
        for phrase in productive_phrases:
            if phrase in response_lower:
                productive_score += 3
        
        if ('como posso ajudar' in response_lower and 
            len(response_text.split()) <= 8 and
            not any(word in response_lower for word in ['verificar', 'analisar', 'resolver'])):
            unproductive_score += 5
        
        logger.info(f"Fallback analysis - Produtivo: {productive_score}, Improdutivo: {unproductive_score}")
        
        if unproductive_score > productive_score:
            return "Improdutivo"
        else:
            return "Produtivo"

    def _calculate_confidence_for_custom_model(self, classification: str, email_text: str = "") -> float:
        base_confidence = 0.85
        email_lower = email_text.lower()
        
        clear_indicators = [
            'obrigado', 'parabéns', 'felicitações',
            'preciso', 'gostaria', 'solicito', 'problema'
        ]
        
        ambiguous_patterns = [
            len(email_text.split()) < 3,
            '?' not in email_text and 'preciso' not in email_lower,
        ]
        
        clarity_bonus = 0.0
        for indicator in clear_indicators:
            if indicator in email_lower:
                clarity_bonus += 0.05
                break
        
        ambiguity_penalty = 0.0
        for pattern in ambiguous_patterns:
            if pattern:
                ambiguity_penalty += 0.08
        
        confidence = base_confidence + clarity_bonus - ambiguity_penalty
        return max(0.70, min(0.95, confidence))

    def get_last_confidence(self) -> float:
        return self.last_confidence