import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { ChatMessage, ChatResponse } from '../shared/models/chat.model';

export type { ChatMessage, ChatResponse };

@Injectable({ providedIn: 'root' })
export class ChatService {
  constructor(private api: ApiService) {}

  sendMessage(message: string, history: ChatMessage[]): Observable<ChatResponse> {
    return this.api.post<ChatResponse>('api/chat', { message, history });
  }
}
