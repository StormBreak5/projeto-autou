# AutoU - Frontend (Classificador de Emails)

Interface web moderna desenvolvida em Angular com Material Design para o sistema de classificação inteligente de emails.

## 🚀 Funcionalidades

- **Interface Material Design**: Design moderno seguindo as diretrizes do Google
- **Upload de Arquivos**: Suporte para arquivos .txt e .pdf com drag & drop
- **Entrada de Texto**: Editor de texto com auto-resize
- **Classificação em Tempo Real**: Feedback visual com spinners e progress bars
- **Respostas Sugeridas**: Geração automática de respostas contextuais
- **Indicador de Confiança**: Barra de progresso visual da precisão
- **Notificações**: Feedback com snackbars do Material Design

## 🛠️ Tecnologias Utilizadas

- **Angular 14**: Framework principal
- **Angular Material 13**: Componentes de UI
- **TypeScript**: Linguagem de programação
- **SCSS**: Estilização avançada
- **RxJS**: Programação reativa
- **Angular Reactive Forms**: Gerenciamento de formulários

## 📋 Pré-requisitos

- Node.js (versão 16 ou superior)
- npm ou yarn
- Angular CLI

## 🔧 Instalação e Configuração

1. **Instalar dependências:**
   ```bash
   npm install
   ```

2. **Instalar Angular CLI (se necessário):**
   ```bash
   npm install -g @angular/cli
   ```

## 🚀 Executando o Projeto

### Servidor de Desenvolvimento
```bash
ng serve
```
Acesse `http://localhost:4200/` no navegador.

### Build para Produção
```bash
ng build --configuration production
```
Os arquivos serão gerados na pasta `dist/`.

### Executar Testes
```bash
ng test
```

## 🏗️ Estrutura do Projeto

```
src/
├── app/
│   ├── services/
│   │   └── email-classification.service.ts  # Serviço de classificação
│   ├── app.component.ts                     # Componente principal
│   ├── app.component.html                   # Template principal
│   ├── app.component.scss                   # Estilos do componente
│   └── app.module.ts                        # Módulo principal
├── environments/
│   ├── environment.ts                       # Configurações de desenvolvimento
│   └── environment.prod.ts                  # Configurações de produção
├── assets/                                  # Recursos estáticos
├── styles.scss                             # Estilos globais
└── index.html                              # Página principal
```

## 🎨 Design System

### Cores Principais
- **Primária**: #2563eb (Azul)
- **Secundária**: #64748b (Cinza)
- **Sucesso**: #059669 (Verde)
- **Aviso**: #d97706 (Laranja)
- **Erro**: #dc2626 (Vermelho)

### Componentes
- **Cards**: Containers com sombra e bordas arredondadas
- **Botões**: Estados hover e disabled
- **Formulários**: Validação visual em tempo real
- **Badges**: Indicadores de categoria com cores contextuais

## 🔌 Integração com Backend

O frontend está preparado para integração com a API Python. Configure a URL do backend no arquivo de ambiente:

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 📱 Responsividade

A interface é totalmente responsiva e otimizada para:
- **Desktop**: Layout completo com sidebar
- **Tablet**: Layout adaptado com navegação colapsável
- **Mobile**: Interface otimizada para toque

## 🧪 Funcionalidades de Teste

O sistema inclui simulação de classificação para testes sem backend:
- Análise de palavras-chave
- Geração de respostas contextuais
- Simulação de tempo de processamento
- Indicadores de confiança realistas

## 🚀 Deploy

### Vercel (Recomendado)
1. Conecte o repositório ao Vercel
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

### Netlify
1. Build: `ng build --configuration production`
2. Pasta de publicação: `dist/frontend`

### Servidor Próprio
1. Execute `ng build --configuration production`
2. Sirva os arquivos da pasta `dist/frontend`

## 🔧 Configurações Avançadas

### Proxy para Desenvolvimento
Crie `proxy.conf.json` na raiz do projeto:
```json
{
  "/api/*": {
    "target": "http://localhost:8000",
    "secure": true,
    "changeOrigin": true
  }
}
```

Execute com: `ng serve --proxy-config proxy.conf.json`

## 📈 Performance

- **Lazy Loading**: Carregamento sob demanda
- **Tree Shaking**: Remoção de código não utilizado
- **Minificação**: Compressão de assets
- **Caching**: Estratégias de cache otimizadas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido para o processo seletivo da AutoU.
