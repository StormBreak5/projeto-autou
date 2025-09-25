from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/classify', methods=['POST'])
def classify_email():
    data = request.get_json()
    email_text = data.get('text', '')

    if "suporte técnico" in email_text.lower():
        classification = "Produtivo"
        suggestion = "Obrigado por entrar em contato. Nossa equipe de suporte técnico já recebeu sua solicitação e retornará em breve."
    else:
        classification = "Improdutivo"
        suggestion = "Agradecemos sua mensagem. Tenha um ótimo dia!"

    return jsonify({
        'category': classification,
        'suggested_response': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)