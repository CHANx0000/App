import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import {
  UserInfoRequest,
  UserInfoRecord,
  UsersListResponse,
} from '../shared/models/user-info.model';

// Re-export so components only need to import from the service
export type { UserInfoRequest, UserInfoRecord, UsersListResponse };

@Injectable({ providedIn: 'root' })
export class UserInfoService {
  constructor(private api: ApiService) {}

  /**
   * POST /api/users
   * Submits a new user record. Returns the created record with server-assigned id.
   *
   * HOW IT WORKS:
   *   this.api.post<UserInfoRecord>('api/users', data)
   *   └─ ApiService.post() handles the HTTP verb, base URL, and headers
   *   └─ <UserInfoRecord> tells TypeScript the shape of the response body
   *   └─ Returns Observable<UserInfoRecord> — subscribe in the component
   */
  createUser(data: UserInfoRequest): Observable<UserInfoRecord> {
    return this.api.post<UserInfoRecord>('api/users', data);
  }

  /**
   * GET /api/users
   * Fetches all previously submitted user records.
   */
  getUsers(): Observable<UsersListResponse> {
    return this.api.get<UsersListResponse>('api/users');
  }
}
