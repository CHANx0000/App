import { Component, signal, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('recruiter-app');
  protected readonly apiStatus = signal<string>('Checking...');
  protected readonly apiConnected = signal<boolean>(false);

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.checkApiConnection();
  }

  private checkApiConnection(): void {
    this.apiService.healthCheck().subscribe({
      next: (response) => {
        this.apiStatus.set(`Connected: ${response.message}`);
        this.apiConnected.set(true);
        console.log('API Connection successful:', response);
      },
      error: (error) => {
        this.apiStatus.set('Failed to connect to API');
        this.apiConnected.set(false);
        console.error('API Connection failed:', error);
      }
    });
  }
}
