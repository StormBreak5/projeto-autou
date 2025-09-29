import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import logging
from services.email_processor import EmailProcessor
from services.ai_classifier import AIClassifier
from services.response_generator import ResponseGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=['*'])

email_processor = EmailProcessor()
ai_classifier = AIClassifier()
response_generator = ResponseGenerator()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'AutoU Email Classifier API is running'})

@app.route('/api/classify', methods=['POST'])
def classify_email():
    start_time = time.time()
    
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            email_text = email_processor.process_file(file)
        else:
            try:
                data = request.get_json(force=True)
            except Exception as json_error:
                logger.error(f"Erro ao decodificar JSON: {str(json_error)}")
                return jsonify({'error': 'JSON inválido ou problema de encoding'}), 400
            
            if not data or 'text' not in data:
                return jsonify({'error': 'Texto do email é obrigatório'}), 400
            email_text = data.get('text', '')

        if not email_text.strip():
            return jsonify({'error': 'Email vazio ou inválido'}), 400

        processed_text = email_processor.preprocess_text(email_text)
        classification = ai_classifier.classify(processed_text)
        suggested_response = response_generator.generate_response(email_text, classification)

        processing_time = round(time.time() - start_time, 3)

        response_data = {
            'original_text': email_text,
            'category': classification,
            'suggested_response': suggested_response,
            'confidence': ai_classifier.get_last_confidence(),
            'processing_time': processing_time
        }
        
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Erro ao processar email: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/classify/batch', methods=['POST'])
def classify_batch():
    try:
        try:
            data = request.get_json(force=True)
        except Exception as json_error:
            logger.error(f"Erro ao decodificar JSON: {str(json_error)}")
            return jsonify({'error': 'JSON inválido ou problema de encoding'}), 400
            
        if not data or 'emails' not in data:
            return jsonify({'error': 'Lista de emails é obrigatória'}), 400

        emails = data.get('emails', [])
        results = []

        for i, email_text in enumerate(emails):
            try:
                item_start_time = time.time()
                processed_text = email_processor.preprocess_text(email_text)
                classification = ai_classifier.classify(processed_text)
                suggested_response = response_generator.generate_response(email_text, classification)
                item_processing_time = round(time.time() - item_start_time, 3)
                
                results.append({
                    'index': i,
                    'category': classification,
                    'suggested_response': suggested_response,
                    'confidence': ai_classifier.get_last_confidence(),
                    'processing_time': item_processing_time
                })
            except Exception as e:
                results.append({'index': i, 'error': str(e)})

        return jsonify({'results': results}), 200

    except Exception as e:
        logger.error(f"Erro ao processar lote de emails: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)