# Guia de Teste - Angular Material

## 🧪 Como Testar a Interface Material

### 1. Iniciar a Aplicação
```bash
cd frontend
ng serve
```
Acesse: `http://localhost:4200` (ou a porta indicada)

### 2. Testar Componentes Material

#### 📱 Toolbar
- ✅ Verificar ícone de email à esquerda
- ✅ Título centralizado "AutoU - Classificador de Emails"
- ✅ Ícone de IA à direita
- ✅ Cor primária (roxo) aplicada

#### 📋 Formulário
- ✅ Radio buttons Material para seleção de método
- ✅ Campo de texto com outline e label flutuante
- ✅ Botão de upload com ícone Material
- ✅ Validação visual em tempo real
- ✅ Botões raised (Classificar) e stroked (Limpar)

#### 📊 Resultados
- ✅ Card com header e ícone
- ✅ Chip colorido para categoria
- ✅ Progress bar para confiança
- ✅ Card aninhado para resposta
- ✅ Botão de cópia com tooltip

#### 🔔 Notificações
- ✅ Snackbar ao copiar resposta
- ✅ Posicionamento centralizado na parte inferior
- ✅ Auto-dismiss após 3 segundos

### 3. Testar Responsividade

#### Desktop (1200px+)
- Layout em grid com 3 colunas para features
- Formulário com campos lado a lado
- Toolbar completa

#### Tablet (768px-1199px)
- Grid de features em 2 colunas
- Formulário em coluna única
- Elementos bem espaçados

#### Mobile (<768px)
- Grid de features em 1 coluna
- Botões em largura total
- Radio buttons empilhados
- Toolbar compacta

### 4. Testar Funcionalidades

#### Entrada de Texto
1. Selecionar "Digitar texto"
2. Colar email de exemplo:
```
Assunto: Problema no sistema

Prezados, estou com um erro crítico no sistema de pagamentos. 
Preciso de suporte urgente para resolver esta questão.

Atenciosamente,
João Silva
```
3. Clicar em "Classificar Email"
4. Verificar spinner durante processamento
5. Verificar resultado "Produtivo" com chip verde

#### Upload de Arquivo
1. Selecionar "Upload arquivo"
2. Clicar no botão de upload
3. Selecionar arquivo `exemplo-email-produtivo.txt`
4. Verificar preview do conteúdo
5. Processar e verificar resultado

#### Cópia de Resposta
1. Após classificação, clicar no ícone de cópia
2. Verificar snackbar de confirmação
3. Colar em editor de texto para confirmar

### 5. Verificar Acessibilidade

#### Navegação por Teclado
- ✅ Tab entre elementos funcionando
- ✅ Enter para ativar botões
- ✅ Espaço para radio buttons
- ✅ Escape para fechar tooltips

#### Leitores de Tela
- ✅ Labels apropriados nos campos
- ✅ Aria-labels nos ícones
- ✅ Estrutura semântica correta
- ✅ Feedback de erro acessível

### 6. Performance Material

#### Carregamento
- ✅ Ícones Material carregam rapidamente
- ✅ Fontes Roboto aplicadas corretamente
- ✅ Animações suaves sem lag
- ✅ Componentes renderizam sem delay

#### Interações
- ✅ Hover states responsivos
- ✅ Ripple effects nos botões
- ✅ Transições suaves entre estados
- ✅ Feedback visual imediato

### 7. Temas e Cores

#### Paleta Material
- **Primary**: Roxo (#673ab7)
- **Accent**: Rosa/Magenta (#e91e63)
- **Warn**: Vermelho padrão Material
- **Background**: Cinza claro (#fafafa)

#### Verificações Visuais
- ✅ Contraste adequado em todos os elementos
- ✅ Cores consistentes com tema escolhido
- ✅ Estados disabled visualmente claros
- ✅ Feedback de erro em vermelho

### 8. Componentes Específicos

#### Mat-Card
```html
<mat-card class="input-card">
  <mat-card-header>
    <mat-card-title>Título com ícone</mat-card-title>
    <mat-card-subtitle>Subtítulo explicativo</mat-card-subtitle>
  </mat-card-header>
  <mat-card-content>Conteúdo</mat-card-content>
</mat-card>
```

#### Mat-Form-Field
```html
<mat-form-field appearance="outline">
  <mat-label>Label</mat-label>
  <textarea matInput></textarea>
  <mat-icon matSuffix>description</mat-icon>
  <mat-error>Mensagem de erro</mat-error>
</mat-form-field>
```

#### Mat-Button
```html
<button mat-raised-button color="primary">
  <mat-icon>psychology</mat-icon>
  Classificar Email
</button>
```

### 9. Debugging Material

#### DevTools
- Inspecionar elementos Material no DOM
- Verificar classes CSS aplicadas
- Testar breakpoints responsivos
- Monitorar performance de animações

#### Console
- Verificar se não há erros Material
- Confirmar imports de módulos
- Validar tema aplicado corretamente

### 10. Checklist Final

- [ ] Todos os componentes Material renderizam
- [ ] Tema Purple/Green aplicado
- [ ] Responsividade funciona em todos os breakpoints
- [ ] Acessibilidade por teclado funcional
- [ ] Snackbars aparecem e desaparecem
- [ ] Ícones Material carregam corretamente
- [ ] Animações suaves e performáticas
- [ ] Formulários validam visualmente
- [ ] Tooltips funcionam no hover
- [ ] Progress bars animam corretamente

---

**Status**: ✅ Interface Material Design completa e funcional
**Próximo passo**: Integração com backend Python