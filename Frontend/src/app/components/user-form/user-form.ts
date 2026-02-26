import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  UserInfoService,
  UserInfoRequest,
  UserInfoRecord,
} from '../../services/user-info.service';

type TabId = 'form' | 'users';

@Component({
  selector: 'app-user-form',
  imports: [FormsModule],
  templateUrl: './user-form.html',
  styleUrl: './user-form.scss',
})
export class UserForm {
  // ── Tab state ─────────────────────────────────────────────────────────────
  activeTab = signal<TabId>('form');

  // ── Form properties (two-way bound via [(ngModel)]) ───────────────────────
  userName = '';
  userAge: number | null = null;
  userGender: 'male' | 'female' | 'other' | '' = '';

  // ── UI state signals ──────────────────────────────────────────────────────
  isSubmitting = signal(false);
  submitSuccess = signal(false);
  submitError = signal<string | null>(null);
  submittedUsers = signal<UserInfoRecord[]>([]);

  constructor(private userInfoService: UserInfoService) {}

  setTab(tab: TabId) {
    this.activeTab.set(tab);
    if (tab === 'users') {
      this.loadUsers();
    }
  }

  isFormValid(): boolean {
    return (
      this.userName.trim().length > 0 &&
      this.userAge !== null &&
      this.userAge >= 0 &&
      this.userAge <= 150 &&
      this.userGender !== ''
    );
  }

  submitUserForm() {
    if (!this.isFormValid()) return;

    const payload: UserInfoRequest = {
      name: this.userName.trim(),
      age: this.userAge as number,
      gender: this.userGender as 'male' | 'female' | 'other',
    };

    this.isSubmitting.set(true);
    this.submitError.set(null);
    this.submitSuccess.set(false);

    this.userInfoService.createUser(payload).subscribe({
      next: () => {
        this.submitSuccess.set(true);
        this.isSubmitting.set(false);
        this.resetForm();
      },
      error: (err) => {
        this.submitError.set(err?.message ?? 'Submission failed. Please try again.');
        this.isSubmitting.set(false);
      },
    });
  }

  private loadUsers() {
    this.userInfoService.getUsers().subscribe({
      next: (response) => this.submittedUsers.set(response.users),
      error: () => this.submittedUsers.set([]),
    });
  }

  private resetForm() {
    this.userName = '';
    this.userAge = null;
    this.userGender = '';
  }
}
