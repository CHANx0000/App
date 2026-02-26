import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { ApiError } from '../../shared/models/api.model';

export const httpInterceptor: HttpInterceptorFn = (req, next) => {
  const modifiedReq = req.clone({
    setHeaders: { 'Content-Type': 'application/json' },
  });

  return next(modifiedReq).pipe(
    catchError((error: HttpErrorResponse) => {
      const apiError: ApiError = {
        status: error.status,
        message: error.error?.detail ?? error.message,
        error: error.error,
      };
      console.error('[HTTP Error]', apiError);
      return throwError(() => apiError);
    })
  );
};
