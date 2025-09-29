import os
import logging
import random
from typing import Dict, List

logger = logging.getLogger(__name__)

class ResponseGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.use_openai = False
        
        if self.openai_api_key:
            try:
                import openai
                if hasattr(openai, 'OpenAI'):
                    self.client = openai.OpenAI(api_key=self.openai_api_key)
                else:
                    openai.api_key = self.openai_api_key
                    self.client = openai
                
                self.use_openai = True
                logger.info("Usando OpenAI para geração de respostas")
            except Exception as e:
                logger.error(f"Erro ao inicializar OpenAI: {str(e)}")
                logger.info("Fallback para templates de resposta")
                self.use_openai = False
        else:
            logger.info("OpenAI não configurado, usando templates de resposta")
        
        self._load_response_templates()
    
    def generate_response(self, email_text: str, classification: str) -> str:
        try:
            if self.use_openai:
                return self._generate_with_openai(email_text, classification)
            else:
                return self._generate_with_templates(email_text, classification)
        except Exception as e:
            logger.error(f"Erro na geração de resposta: {str(e)}")
            return self._generate_with_templates(email_text, classification)
    
    def _generate_with_openai(self, email_text: str, classification: str) -> str:
        try:
            prompt = self._build_response_prompt(email_text, classification)
            
            if hasattr(self.client, 'chat') and hasattr(self.client.chat, 'completions'):
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self._get_response_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self._get_response_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Erro na geração OpenAI: {str(e)}")
            raise
    
    def _generate_with_templates(self, email_text: str, classification: str) -> str:
        email_lower = email_text.lower()
        
        if classification == "Produtivo":
            return self._get_productive_response(email_lower)
        else:
            return self._get_unproductive_response(email_lower)
    
    def _get_productive_response(self, email_text: str) -> str:
        if any(word in email_text for word in ['suporte', 'técnico', 'problema', 'erro', 'bug']):
            templates = self.response_templates['productive']['technical_support']
        elif any(word in email_text for word in ['status', 'andamento', 'atualização']):
            templates = self.response_templates['productive']['status_request']
        elif any(word in email_text for word in ['dúvida', 'questão', 'pergunta']):
            templates = self.response_templates['productive']['question']
        elif any(word in email_text for word in ['documento', 'arquivo', 'relatório']):
            templates = self.response_templates['productive']['document_request']
        else:
            templates = self.response_templates['productive']['general']
        
        return random.choice(templates)
    
    def _get_unproductive_response(self, email_text: str) -> str:
        if any(word in email_text for word in ['obrigado', 'agradecimento', 'grato']):
            templates = self.response_templates['unproductive']['thanks']
        elif any(word in email_text for word in ['parabéns', 'felicitações', 'aniversário']):
            templates = self.response_templates['unproductive']['congratulations']
        elif any(word in email_text for word in ['natal', 'ano novo', 'feriado']):
            templates = self.response_templates['unproductive']['holidays']
        else:
            templates = self.response_templates['unproductive']['general']
        
        return random.choice(templates)
    
    def _load_response_templates(self):
        self.response_templates = {
            'productive': {
                'technical_support': [
                    "Obrigado por entrar em contato conosco. Recebemos sua solicitação de suporte técnico e nossa equipe especializada já foi notificada. Retornaremos com uma solução em até 24 horas úteis.",
                    "Sua solicitação de suporte foi registrada com sucesso. Nossa equipe técnica está analisando o problema reportado e entrará em contato em breve com uma solução.",
                    "Agradecemos por reportar este problema técnico. Já encaminhamos sua solicitação para nossa equipe de desenvolvimento e você receberá uma resposta detalhada em breve."
                ],
                'status_request': [
                    "Obrigado por sua solicitação de atualização. Estamos verificando o status atual de sua requisição e retornaremos com informações detalhadas em breve.",
                    "Recebemos sua solicitação de status. Nossa equipe está compilando as informações mais recentes e enviaremos um relatório completo nas próximas horas.",
                    "Sua solicitação de atualização foi recebida. Estamos consultando os responsáveis pelo projeto e retornaremos com o status atual em breve."
                ],
                'question': [
                    "Obrigado por sua pergunta. Nossa equipe está analisando sua dúvida e retornará com uma resposta detalhada em breve.",
                    "Recebemos sua questão e já a encaminhamos para o especialista responsável. Você receberá uma resposta completa nas próximas horas.",
                    "Agradecemos por entrar em contato. Sua dúvida está sendo analisada por nossa equipe e retornaremos com esclarecimentos em breve."
                ],
                'document_request': [
                    "Sua solicitação de documento foi recebida. Estamos preparando os arquivos solicitados e os enviaremos em breve.",
                    "Obrigado por sua solicitação. Os documentos estão sendo compilados e você os receberá nas próximas horas.",
                    "Recebemos sua solicitação de documentação. Nossa equipe está organizando os arquivos e os enviará em breve."
                ],
                'general': [
                    "Obrigado por entrar em contato conosco. Sua solicitação foi recebida e nossa equipe retornará em breve com as informações necessárias.",
                    "Recebemos sua mensagem e já a encaminhamos para o departamento responsável. Retornaremos com uma resposta em breve.",
                    "Agradecemos por seu contato. Sua solicitação está sendo analisada e você receberá uma resposta detalhada nas próximas horas."
                ]
            },
            'unproductive': {
                'thanks': [
                    "Muito obrigado por suas palavras gentis! Ficamos felizes em poder ajudar. Estamos sempre à disposição.",
                    "Agradecemos imensamente por seu feedback positivo. É um prazer trabalhar com você!",
                    "Suas palavras de agradecimento são muito importantes para nós. Obrigado por reconhecer nosso trabalho!"
                ],
                'congratulations': [
                    "Muito obrigado pelas felicitações! Ficamos honrados com suas palavras gentis.",
                    "Agradecemos imensamente por suas felicitações. Suas palavras são muito importantes para nós!",
                    "Obrigado pelas parabenizações! É sempre um prazer receber mensagens tão positivas."
                ],
                'holidays': [
                    "Muito obrigado pelos votos de boas festas! Desejamos a você e sua família momentos de muita alegria e prosperidade.",
                    "Agradecemos pelos cumprimentos festivos! Que este período seja repleto de paz e felicidade para você.",
                    "Obrigado pelas felicitações! Desejamos que você tenha festividades maravilhosas ao lado de quem ama."
                ],
                'general': [
                    "Obrigado por sua mensagem! Ficamos felizes em receber seu contato. Tenha um excelente dia!",
                    "Agradecemos por entrar em contato conosco. Sua mensagem é muito importante para nós!",
                    "Muito obrigado por sua mensagem gentil. Estamos sempre à disposição quando precisar!"
                ]
            }
        }
    
    def _build_response_prompt(self, email_text: str, classification: str) -> str:
        return f"""
        Gere uma resposta automática profissional e adequada para o seguinte email classificado como "{classification}":

        Email original: "{email_text}"

        Diretrizes:
        - Para emails "Produtivos": Confirme o recebimento, indique que a solicitação será analisada e dê um prazo estimado
        - Para emails "Improdutivos": Seja cordial, agradeça pela mensagem e mantenha um tom amigável
        - Use linguagem formal mas acolhedora
        - Seja conciso (máximo 3 frases)
        - Inclua uma saudação apropriada

        Resposta:
        """
    
    def _get_response_system_prompt(self) -> str:
        return """
        Você é um assistente especializado em gerar respostas automáticas profissionais para emails corporativos.
        Suas respostas devem ser cordiais, profissionais e adequadas ao contexto do email recebido.
        Mantenha sempre um tom respeitoso e prestativo.
        """