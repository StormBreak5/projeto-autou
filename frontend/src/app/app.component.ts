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
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.emailForm.patchValue({ inputMethod: 'file' });
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        this.emailForm.patchValue({ emailText: content });
      };
      reader.readAsText(file);
    }
  }

  onSubmit() {
    if (this.emailForm.valid) {
      this.isProcessing = true;
      this.error = null;
      this.result = null;

      const request = {
        text: this.emailForm.value.emailText,
        file: this.selectedFile && this.emailForm.value.inputMethod === 'file' ? this.selectedFile : undefined
      };

      this.emailService.classifyEmail(request).subscribe({
        next: (result) => {
          this.result = result;
          this.isProcessing = false;
        },
        error: (error) => {
          this.error = 'Erro ao processar o email. Tente novamente.';
          this.isProcessing = false;
          console.error('Classification error:', error);
        }
      });
    }
  }

  clearForm() {
    this.emailForm.reset();
    this.emailForm.patchValue({ inputMethod: 'text' });
    this.selectedFile = null;
    this.result = null;
    this.error = null;
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
