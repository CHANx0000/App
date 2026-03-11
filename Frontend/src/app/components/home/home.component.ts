import { Component, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-home',
  imports: [RouterLink],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit {
  apiConnected = signal<boolean | null>(null);

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.healthCheck().subscribe({
      next: () => this.apiConnected.set(true),
      error: () => this.apiConnected.set(false),
    });
  }
}
