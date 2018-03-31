import { ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot } from '@angular/router';
import { Injectable } from '@angular/core';

import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs/Observable';


/*
NOTE! Important to add the service to providers field in app module!
NOTE! This guard should be stated on the top level route of the section you want to protect in the app-routing module
      by filling in the field 'canActivate: [<Guard>, <Guard>...]'
 */

@Injectable()
export class AuthGuardService implements CanActivate, CanActivateChild {
  // Inject the authentication service to use with canActivate
  constructor(private authService: AuthService,
              private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<boolean> | Promise<boolean> | boolean {
    return this.authService.isAuthenticated()
      .then(
        (authenticated: boolean) => {
          if (authenticated) {
            return true;
          } else {
            this.router.navigate(['/auth']);
          }
        }
      );
  }

  canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<boolean> | Promise<boolean> | boolean {
    return this.authService.isAuthenticated()
      .then(
          (authenticated: boolean) => {
            if (authenticated) {
              return true;
            } else {
              this.router.navigate(['/auth']);
            }
          }
        );
  }
}
