import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { UsersService } from '../../services/users.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
})
export class Login {
  isLoading = false;
  loginError = '';

  credentials = {
    username: '',
    password: '',
  };

  constructor(
    private usersService: UsersService,
    private router: Router,
  ) {}

  onLogin() {
    // prevent multiple clicks while processing login
    if (this.isLoading) return;
    // Validate that fields are not empty
    if (!this.credentials.username || !this.credentials.password) {
      this.loginError = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.loginError = '';

    this.usersService.login(this.credentials.username, this.credentials.password).subscribe({
      next: (response) => {
        if (response?.access) {
          localStorage.setItem('access_token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          this.router.navigate(['/movies']);
          this.credentials.password = ''; // Clear password after successful login
        }
      },
      error: (error) => {
        console.error('Login error:', error);

        if (error.status === 401) {
          this.loginError = 'Incorrect username or password';
        } else if (error.status === 0) {
          this.loginError = 'Connection error. Please check if the server is running';
        } else {
          this.loginError = 'Error logging in. Please try again';
        }
        this.isLoading = false;
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  createAccount() {
    // Navigate to the registration page
    this.router.navigate(['/users/create']);
  }

}
