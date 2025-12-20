import { inject } from '@angular/core';
import { UsersService } from './users.service';
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, switchMap } from 'rxjs/operators';
import { throwError } from 'rxjs';

export const usersInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access_token');
  const authReq = token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req;

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && error.error?.code === 'token_not_valid') {
        const usersService = inject(UsersService);
        return usersService.refreshToken().pipe(
          switchMap(({ access }) => {
            localStorage.setItem('access_token', access);
            const retryReq = req.clone({ setHeaders: { Authorization: `Bearer ${access}` } });
            return next(retryReq);
          })
        );
      }
      return throwError(() => error);
    })
  );
};