import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { baseUrl } from './config';
import { User } from '../models/users.model';

@Injectable({ providedIn: 'root' })
export class UsersService {
  private api = `${baseUrl}users/`;
  private authApi = `${baseUrl}auth/`;

  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.getCurrentUser().subscribe({ error: () => this.logout() });
    }
  }

  login(username: string, password: string): Observable<{ access: string; refresh: string }> {
    return this.http.post<{ access: string; refresh: string }>(`${this.authApi}login/`, { username, password }).pipe(
      tap((res) => {
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('refresh_token', res.refresh);
        // Load and emit current user after login
        this.getCurrentUser().subscribe();
      }),
      catchError((err) => {
        console.error('Login error:', err);
        return throwError(() => err);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
    this.currentUserSubject.next(null);
  }

  // Create user (registration)
  register(userData: Partial<User>): Observable<User> {
    return this.http.post<User>(this.api, userData);
  }

  // Current user (adjust if your backend uses another endpoint)
  getCurrentUser(): Observable<User> {
    // If you don’t have /users/me/, decode user_id from JWT and call /users/{id}/
    const token = localStorage.getItem('access_token');
    const id = token ? this.decodeUserIdFromToken(token) : null;
    if (!id) {
      return throwError(() => new Error('No access token or user_id'));
    }
    return this.http.get<User>(`${this.api}${id}/`).pipe(
      tap((user) => {
        this.currentUserSubject.next(user);
        localStorage.setItem('current_user', JSON.stringify(user));
      })
    );
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.api}${id}/`);
  }

  // Partial update (PATCH) to avoid 400 requiring all fields (e.g., password)
  updateUser(id: number, payload: Partial<User>): Observable<User> {
    return this.http.patch<User>(`${this.api}${id}/`, payload);
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.api}${id}/`);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  refreshToken(): Observable<{ access: string }> {
    const refresh = localStorage.getItem('refresh_token');
    return this.http.post<{ access: string }>(`${baseUrl}token/refresh/`, { refresh });
  }

  private decodeUserIdFromToken(token: string): number | null {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.user_id || payload.sub || null;
    } catch {
      return null;
    }
  }
}