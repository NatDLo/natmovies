import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { UsersService } from './services/users.service';
import { Observable } from 'rxjs';
import { User } from './models/users.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './app.html',
})
export class App implements OnInit{
  currentUser$: Observable<User | null>;

  constructor(private users: UsersService, private router: Router) {
    this.currentUser$ = this.users.currentUser$;
  }

  ngOnInit(): void {
    // if there's a token, load the user on start
    if (this.users.isAuthenticated()) {
      this.users.getCurrentUser().subscribe({ error: () => this.users.logout() });
    }
  }

  get isAuthenticated(): boolean {
    return this.users.isAuthenticated();
  }

  logout() {
    this.users.logout();
    this.router.navigate(['/login']);
  }

  goToProfile() {
    this.router.navigate(['/profile']);
  }
}