import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-input-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './input-form.component.html',
  styleUrl: './input-form.component.scss',
})
export class InputFormComponent {
  inputText = signal('');

  constructor(private http: HttpClient) {}

  onSubmit() {
    const text = this.inputText();

    // Send the text to your backend
    this.http.post('/api/submit', { text }).subscribe({
      next: (response) => {
        console.log('Success:', response);
        // Clear input after successful submission
        this.inputText.set('');
      },
      error: (error) => {
        console.error('Error:', error);
      },
    });
  }

  updateInput(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.inputText.set(value);
  }
}
