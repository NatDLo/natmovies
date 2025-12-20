import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { UsersService } from '../../services/users.service';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from '../../models/users.model';

@Component({
  selector: 'app-users-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './users-form.html',
})
export class UserForm implements OnInit {
  userForm: FormGroup;
  userId: number | null = null;
  editMode = false;
  title = 'Create Account';

  constructor(
    private usersService: UsersService,
    private router: Router,
    private route: ActivatedRoute,
    private fb: FormBuilder,
  ) {
    this.userForm = this.fb.group({
      username: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      first_name: [''],
      last_name: [''],
      password: [''], // required only on create
    });
  }

  ngOnInit() {
    const isCreate = this.router.url.includes('/users/create');
    const isProfile = this.router.url.startsWith('/profile');
    const idParam = this.route.snapshot.paramMap.get('id');

    if (isCreate) {
      this.editMode = false;
      this.title = 'Create Account';
      this.userForm.get('password')?.setValidators([Validators.required, Validators.minLength(6)]);
      this.userForm.get('password')?.updateValueAndValidity();
      return;
    }

    if (isProfile) {
      this.editMode = true;
      this.title = 'Edit Profile';
      this.usersService.getCurrentUser().subscribe({
        next: (user: User) => {
          this.userId = user?.id ?? null;
          if (this.userId) {
            this.userForm.patchValue({
              username: user.username,
              email: user.email,
              first_name: user.first_name,
              last_name: user.last_name,
            });
          }
        },
        error: (e) => console.error('Failed to load current user', e),
      });
      this.userForm.get('password')?.clearValidators();
      this.userForm.get('password')?.updateValueAndValidity();
      return;
    }

    if (idParam) {
      const id = Number(idParam);
      if (!Number.isNaN(id)) {
        this.editMode = true;
        this.title = 'Edit User';
        this.userId = id;
        this.usersService.getUser(id).subscribe({
          next: (user) => {
            this.userForm.patchValue({
              username: user.username,
              email: user.email,
              first_name: user.first_name,
              last_name: user.last_name,
            });
          },
          error: (e) => console.error('Failed to load user', e),
        });
        this.userForm.get('password')?.clearValidators();
        this.userForm.get('password')?.updateValueAndValidity();
      }
    }
  }

  updateUser(): void {
    if (this.userForm.invalid) {
      this.userForm.markAllAsTouched();
      return;
    }
    const v = this.userForm.value;

    if (this.editMode && this.userId) {
      const payload: Partial<User> = {
        username: v.username,
        email: v.email,
        first_name: v.first_name,
        last_name: v.last_name,
      };
      // include password only if provided and valid
      if (v.password && String(v.password).trim().length >= 6) {
        payload.password = v.password;
      }
      this.usersService.updateUser(this.userId, payload).subscribe({
        next: () => this.router.navigate(['/movies']),
        error: (e) => {
          console.error('Update error', e?.error ?? e);
          alert(typeof e?.error === 'string' ? e.error : JSON.stringify(e?.error));
        },
      });
    } else {
      const payload: Partial<User> = {
        username: v.username,
        email: v.email,
        first_name: v.first_name,
        last_name: v.last_name,
        password: v.password,
      };
      this.usersService.register(payload).subscribe({
        next: () => this.router.navigate(['/login']),
        error: (e) => {
          console.error('Create error', e?.error ?? e);
          alert(typeof e?.error === 'string' ? e.error : JSON.stringify(e?.error));
        },
      });
    }
  }

  deleteUser() {
    if (!this.editMode || !this.userId) return;
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      this.usersService.deleteUser(this.userId).subscribe({
        next: () => {
          alert('User deleted successfully');
          this.usersService.logout();
          this.router.navigate(['/login']);
        },
        error: (error) => {
          console.error('Error deleting user', error);
          alert('Error deleting user. Please try again.');
        },
      });
    }
  }

  navigateToMovies() {
    this.router.navigate(['/movies']);
  }
}