import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { InputFormComponent } from './components/input-form/input-form.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, InputFormComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('Frontend');
}
