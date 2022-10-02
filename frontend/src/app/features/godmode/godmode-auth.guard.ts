import { ActivatedRouteSnapshot, CanActivate, CanActivateChild, Router, RouterStateSnapshot } from '@angular/router';
import { Injectable } from '@angular/core';

import { AuthService } from '../../core/auth/auth.service';
import { Observable } from 'rxjs';
import {User, UserService} from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class GodmodeAuthGuard implements CanActivate, CanActivateChild {
  // Inject the authentication service to use with canActivate
  constructor(private authService: AuthService,
              private userService: UserService,
              private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
    Observable<boolean> | Promise<boolean> | boolean {
    return this.authService.isAuthenticated()
      .then(
        (authenticated: boolean) => {
          if (authenticated) {
            return this.userService.getUser()
              .then((user: User) => {
                console.log("user is super?", user.is_superuser);
                return user.is_superuser;
              })
          } else {
            this.router.navigate(['/']);
            return false;
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
            this.router.navigate(['/']);
            return false;
          }
        }
      );
  }
}
