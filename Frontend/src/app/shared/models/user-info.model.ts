// What we send to POST /api/users
export interface UserInfoRequest {
  name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
}

// What the backend returns for a single user record
export interface UserInfoRecord {
  id: number;
  name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
}

// Shape of GET /api/users response
export interface UsersListResponse {
  users: UserInfoRecord[];
}
