import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Utility } from '../utility';

/*
Interceptors are listed as providers in the root module, AppModule, as they need additional parameters other than where
in the module hierarchy they should be injected.
*/
@Injectable()
export class AuthRequestInterceptor implements HttpInterceptor {
  constructor() {}

  /**
   * This function will be called upon each outgoing HTTP request and will
   * insert the 'X-CSRFToken' header on each request. See
   * https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax for additional
   * information.
   *
   * The X-CSRFToken is both used to mitigate Cross Site Request Forgeries, and
   * also works to identify the current user if he/she is logged in. Upon a
   * user authenticating, the user's CSRF Token can then be used to
   * authenticate them, instead of having to provide username/password with
   * each outgoing HTTP request.
   *
   * This interceptor is registered in the AppModule Angular Module.
   *
   * @param req: HTTP request to modify
   * @param next: Handler
   */
  intercept(req: HttpRequest<any>,
            next: HttpHandler): Observable<HttpEvent<any>> {
    const clonedReq = req.clone({
      headers: req.headers.set('X-CSRFToken', Utility.getCSRFToken())
    });

    return next.handle(clonedReq);
  }
}
