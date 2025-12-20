import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { UsersService } from '../services/users.service';

@Injectable({ providedIn: 'root' })
export class UsersGuard implements CanActivate {
  constructor(
    private usersService: UsersService,
    private router: Router,
  ) {}

  // This guard protects routes to ensure that only 
  // authenticated users can access them.
    canActivate(): boolean {
        if (this.usersService.isAuthenticated()) {
            return true;
        } else {
            this.router.navigate(['/login']);
            return false;
        }
    }
}