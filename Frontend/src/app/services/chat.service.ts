import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  message: string;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  constructor(private api: ApiService) {}

  sendMessage(message: string, history: ChatMessage[]): Observable<ChatResponse> {
    return this.api.post<ChatResponse>('api/chat', { message, history });
  }
}
