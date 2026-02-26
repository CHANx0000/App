import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home';
import { ChatComponent } from './pages/chat/chat';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'chat', component: ChatComponent },
  { path: '**', redirectTo: '' },
];
