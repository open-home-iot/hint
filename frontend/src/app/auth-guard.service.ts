import {ActivatedRouteSnapshot, CanActivate, CanActivateChild, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs/Observable';
import {Injectable} from '@angular/core';

/*
NOTE! Important to add the service to providers field in app module!
NOTE! This guard should be stated on the top level route of the section you want to protect in the app-routing module
      by filling in the field 'canActivate: [<Guard>, <Guard>...]'
 */

// Injectable to be able to inject an authentication service into here.
@Injectable()
export class AuthGuardService implements CanActivate, CanActivateChild {
  // Inject the authentication service to use with canActivate
  constructor() {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<boolean> | Promise<boolean> | boolean {
    // Currently not authenticating for real...
    return true;
  }

  canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<boolean> | Promise<boolean> | boolean {
    // Currently not authenticating for real...
    return true;
  }
}
