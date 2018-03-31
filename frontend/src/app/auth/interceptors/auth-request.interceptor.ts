import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs/Observable';

import { RequestService } from '../../api-interface/request.service';


@Injectable()
export class AuthRequestInterceptor implements HttpInterceptor {
  constructor(private requestService: RequestService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const clonedReq = req.clone({
      headers: req.headers.set('X-CSRFToken', this.requestService.getCSRFToken()),
      // This will allow the CSRF token to be set by the custom pre-flight request. If left out, the CSRF cookie will
      // not be set.
      withCredentials: true});


    return next.handle(clonedReq);
  }
}
