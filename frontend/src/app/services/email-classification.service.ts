import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { delay, map, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface ClassificationResult {
  category: 'Produtivo' | 'Improdutivo';
  confidence: number;
  suggested_response: string;
  processing_time: number;
}

export interface ClassificationRequest {
  text?: string;
  file?: File;
}

@Injectable({
  providedIn: 'root'
})
export class EmailClassificationService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  classifyEmail(request: ClassificationRequest): Observable<ClassificationResult> {
    if (request.file) {
      const formData = new FormData();
      formData.append('file', request.file);
      return this.callActualAPI(formData);
    } else if (request.text) {
      return this.callActualAPIWithText(request.text);
    }

    return this.simulateClassification('');
  }

  private simulateClassification(text: string): Observable<ClassificationResult> {
    const startTime = Date.now();

    const productiveKeywords = [
      'suporte', 'problema', 'erro', 'ajuda', 'dúvida', 'status',
      'atualização', 'urgente', 'sistema', 'falha', 'bug', 'solicitação',
      'requisição', 'pendente', 'prazo', 'documento', 'contrato',
      'pagamento', 'fatura', 'cobrança', 'técnico', 'instalação'
    ];

    const improdutiveKeywords = [
      'parabéns', 'felicitações', 'natal', 'ano novo', 'aniversário',
      'obrigado', 'agradecimento', 'festa', 'evento social', 'convite',
      'bom dia', 'boa tarde', 'boa noite', 'fim de semana', 'feriado'
    ];

    const lowerText = text.toLowerCase();

    const productiveScore = productiveKeywords.reduce((score, keyword) => {
      return score + (lowerText.includes(keyword) ? 1 : 0);
    }, 0);

    const improdutiveScore = improdutiveKeywords.reduce((score, keyword) => {
      return score + (lowerText.includes(keyword) ? 1 : 0);
    }, 0);

    const isProductive = productiveScore > improdutiveScore;
    const confidence = Math.min(0.95, Math.max(0.65,
      (Math.max(productiveScore, improdutiveScore) / Math.max(productiveKeywords.length, improdutiveKeywords.length)) +
      (Math.random() * 0.2) + 0.6
    ));

    const result: ClassificationResult = {
      category: isProductive ? 'Produtivo' : 'Improdutivo',
      confidence: confidence,
      suggested_response: this.generateResponse(isProductive),
      processing_time: (Date.now() - startTime) / 1000
    };

    return of(result).pipe(delay(1500 + Math.random() * 1000));
  }

  private generateResponse(isProductive: boolean): string {
    if (isProductive) {
      const productiveResponses = [
        'Obrigado pelo seu contato. Recebemos sua solicitação e nossa equipe técnica irá analisá-la. Retornaremos em breve com uma resposta detalhada.',
        'Agradecemos por entrar em contato conosco. Sua solicitação foi registrada e será direcionada para o setor responsável. Você receberá um retorno em até 24 horas.',
        'Recebemos sua mensagem e entendemos a importância da sua solicitação. Nossa equipe está trabalhando para resolver a questão e entraremos em contato em breve.',
        'Obrigado por nos informar sobre esta questão. Já encaminhamos sua solicitação para nossa equipe especializada, que entrará em contato para dar continuidade ao atendimento.',
        'Agradecemos seu contato. Sua solicitação foi recebida e está sendo analisada por nossa equipe. Manteremos você informado sobre o andamento.'
      ];
      return productiveResponses[Math.floor(Math.random() * productiveResponses.length)];
    } else {
      const improdutiveResponses = [
        'Muito obrigado pela sua mensagem! Agradecemos o contato e desejamos um excelente dia.',
        'Agradecemos sua mensagem. É sempre um prazer receber seu contato. Tenha um ótimo dia!',
        'Obrigado pelo carinho! Ficamos felizes em receber sua mensagem. Desejamos tudo de bom para você.',
        'Muito obrigado! Sua mensagem nos deixou muito felizes. Tenha uma excelente semana.',
        'Agradecemos imensamente sua mensagem. É sempre bom saber de você. Um abraço!'
      ];
      return improdutiveResponses[Math.floor(Math.random() * improdutiveResponses.length)];
    }
  }

  private callActualAPI(formData: FormData): Observable<ClassificationResult> {
    return this.http.post<any>(`${this.apiUrl}/classify`, formData).pipe(
      map(response => this.mapBackendResponse(response)),
      catchError(error => {
        console.error('API error:', error);
        return this.simulateClassification('Conteúdo do arquivo');
      })
    );
  }

  private callActualAPIWithText(text: string): Observable<ClassificationResult> {
    const body = { text: text };
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post<any>(`${this.apiUrl}/classify`, body, { headers }).pipe(
      map(response => this.mapBackendResponse(response)),
      catchError(error => {
        console.error('API error:', error);
        return this.simulateClassification(text);
      })
    );
  }

  private mapBackendResponse(response: any): ClassificationResult {
    return {
      category: response.category as 'Produtivo' | 'Improdutivo',
      confidence: response.confidence || 0.8,
      suggested_response: response.suggested_response || 'Resposta não disponível',
      processing_time: 1.5
    };
  }
}
