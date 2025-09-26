from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from config import config
from services.email_processor import EmailProcessor
from services.ai_classifier import AIClassifier
from services.response_generator import ResponseGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config_name = os.environ.get('FLASK_ENV', 'default')
app_config = config[config_name]

app = Flask(__name__)
app.config.from_object(app_config)
CORS(app, origins=app_config.CORS_ORIGINS)

email_processor = EmailProcessor()
ai_classifier = AIClassifier()
response_generator = ResponseGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'AutoU Email Classifier API is running'})

@app.route('/classify', methods=['POST'])
def classify_email():
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            email_text = email_processor.process_file(file)
        else:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({'error': 'Texto do email é obrigatório'}), 400
            email_text = data.get('text', '')

        if not email_text.strip():
            return jsonify({'error': 'Email vazio ou inválido'}), 400

        processed_text = email_processor.preprocess_text(email_text)
        classification = ai_classifier.classify(processed_text)
        suggested_response = response_generator.generate_response(email_text, classification)

        return jsonify({
            'original_text': email_text,
            'category': classification,
            'suggested_response': suggested_response,
            'confidence': ai_classifier.get_last_confidence()
        })

    except Exception as e:
        logger.error(f"Erro ao processar email: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/classify/batch', methods=['POST'])
def classify_batch():
    try:
        data = request.get_json()
        if not data or 'emails' not in data:
            return jsonify({'error': 'Lista de emails é obrigatória'}), 400

        emails = data.get('emails', [])
        results = []

        for i, email_text in enumerate(emails):
            try:
                processed_text = email_processor.preprocess_text(email_text)
                classification = ai_classifier.classify(processed_text)
                suggested_response = response_generator.generate_response(email_text, classification)
                
                results.append({
                    'index': i,
                    'category': classification,
                    'suggested_response': suggested_response,
                    'confidence': ai_classifier.get_last_confidence()
                })
            except Exception as e:
                results.append({'index': i, 'error': str(e)})

        return jsonify({'results': results})

    except Exception as e:
        logger.error(f"Erro ao processar lote de emails: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)