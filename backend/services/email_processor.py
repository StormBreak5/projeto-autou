import re
import nltk
import PyPDF2
from io import BytesIO
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class EmailProcessor:
    def __init__(self):
        # Best-effort: ensure NLTK resources if available, but never fail startup on serverless
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        try:
            # If resources are already present, nothing to do
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            # Attempt download, but ignore failures to keep function responsive on Vercel
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
            except Exception as e:
                logger.warning(f"Falha ao baixar dados NLTK (ignorado): {str(e)}")
    
    def process_file(self, file) -> str:
        try:
            filename = file.filename.lower()
            
            if filename.endswith('.txt'):
                return file.read().decode('utf-8')
            elif filename.endswith('.pdf'):
                return self._extract_pdf_text(file)
            else:
                raise ValueError(f"Formato de arquivo não suportado: {filename}")
                
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {file.filename}: {str(e)}")
            raise
    
    def _extract_pdf_text(self, file) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
            raise ValueError("Erro ao processar arquivo PDF")
    
    def preprocess_text(self, text: str) -> str:
        try:
            text = re.sub(r'[^\w\s\.\,\!\?\-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\n+', '\n', text)
            processed_text = text.lower().strip()
            return processed_text
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento: {str(e)}")
            return text
    
    def extract_email_features(self, text: str) -> dict:
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'has_question': '?' in text,
            'has_urgency': any(word in text.lower() for word in [
                'urgente', 'imediato', 'asap', 'prioridade', 'emergência'
            ]),
            'has_greeting': any(word in text.lower() for word in [
                'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite'
            ]),
            'has_thanks': any(word in text.lower() for word in [
                'obrigado', 'obrigada', 'agradeço', 'grato', 'grata'
            ]),
            'has_request': any(word in text.lower() for word in [
                'solicito', 'preciso', 'gostaria', 'poderia', 'favor'
            ])
        }
        
        return features