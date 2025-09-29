import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EmailClassificationService, ClassificationResult } from './services/email-classification.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'AutoU - Classificador de Emails';
  emailForm: FormGroup;
  isProcessing = false;
  result: ClassificationResult | null = null;
  error: string | null = null;
  selectedFile: File | null = null;

  constructor(
    private fb: FormBuilder, 
    private emailService: EmailClassificationService,
    private snackBar: MatSnackBar
  ) {
    this.emailForm = this.fb.group({
      emailText: ['', [Validators.required, Validators.minLength(10)]],
      inputMethod: ['text', Validators.required]
    });

    this.emailForm.get('inputMethod')?.valueChanges.subscribe(method => {
      this.onInputMethodChange(method);
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const allowedTypes = ['text/plain', 'application/pdf'];
      if (!allowedTypes.includes(file.type) && !file.name.endsWith('.txt') && !file.name.endsWith('.pdf')) {
        this.snackBar.open('Tipo de arquivo não suportado. Use apenas .txt ou .pdf', 'Fechar', {
          duration: 4000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom'
        });
        return;
      }

      if (file.size > 5 * 1024 * 1024) {
        this.snackBar.open('Arquivo muito grande. Tamanho máximo: 5MB', 'Fechar', {
          duration: 4000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom'
        });
        return;
      }

      this.selectedFile = file;
      this.emailForm.patchValue({ inputMethod: 'file' });
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        this.emailForm.patchValue({ emailText: content });
      };
      reader.onerror = () => {
        this.snackBar.open('Erro ao ler o arquivo', 'Fechar', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom'
        });
      };
      reader.readAsText(file);
    }
  }

  onSubmit() {
    const inputMethod = this.emailForm.value.inputMethod;
    const emailText = this.emailForm.value.emailText;
    
    let isValid = false;
    if (inputMethod === 'text') {
      isValid = emailText && emailText.trim().length >= 10;
    } else if (inputMethod === 'file') {
      isValid = this.selectedFile && emailText && emailText.trim().length >= 10;
    }

    if (!isValid) {
      let errorMessage = 'Por favor, ';
      if (inputMethod === 'text') {
        errorMessage += 'digite o conteúdo do email (mínimo 10 caracteres)';
      } else {
        errorMessage += 'selecione um arquivo válido';
      }
      
      this.snackBar.open(errorMessage, 'Fechar', {
        duration: 4000,
        horizontalPosition: 'center',
        verticalPosition: 'bottom'
      });
      return;
    }

    this.isProcessing = true;
    this.error = null;
    this.result = null;

    const request = {
      text: emailText,
      file: this.selectedFile && inputMethod === 'file' ? this.selectedFile : undefined
    };

    this.emailService.classifyEmail(request).subscribe({
      next: (result) => {
        this.result = result;
        this.isProcessing = false;
        setTimeout(() => {
          const resultElement = document.querySelector('.results-section');
          if (resultElement) {
            resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      },
      error: (error) => {
        this.error = 'Erro ao processar o email. Verifique sua conexão e tente novamente.';
        this.isProcessing = false;
        console.error('Classification error:', error);
      }
    });
  }

  clearForm() {
    this.emailForm.reset();
    this.emailForm.patchValue({ inputMethod: 'text' });
    this.selectedFile = null;
    this.result = null;
    this.error = null;
    
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
    this.snackBar.open('Formulário limpo', 'Fechar', {
      duration: 2000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom'
    });
  }

  onInputMethodChange(method: string) {
    if (method === 'text') {
      this.selectedFile = null;
      this.emailForm.patchValue({ emailText: '' });
    } else if (method === 'file') {
      this.emailForm.patchValue({ emailText: '' });
    }
  }

  removeFile() {
    this.selectedFile = null;
    this.emailForm.patchValue({ emailText: '' });
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }

  get isFormValid(): boolean {
    const inputMethod = this.emailForm.value.inputMethod;
    const emailText = this.emailForm.value.emailText;
    
    if (inputMethod === 'text') {
      return emailText && emailText.trim().length >= 10;
    } else if (inputMethod === 'file') {
      return this.selectedFile && emailText && emailText.trim().length >= 10;
    }
    
    return false;
  }

  copyResponse() {
    if (this.result?.suggested_response) {
      navigator.clipboard.writeText(this.result.suggested_response).then(() => {
        this.snackBar.open('Resposta copiada para a área de transferência!', 'Fechar', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom'
        });
      }).catch(err => {
        this.snackBar.open('Erro ao copiar texto', 'Fechar', {
          duration: 3000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom'
        });
        console.error('Erro ao copiar texto:', err);
      });
    }
  }
}
