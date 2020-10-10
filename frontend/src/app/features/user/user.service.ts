import { Injectable } from '@angular/core';

import { Subscription } from 'rxjs';

import { HttpService } from '../../core/http/http.service';
import { AuthService } from '../../core/auth/auth.service'

const USER_SELF_URL = window.location.origin + "/api/user/self";


export class User {
  email: string = "";
  firstName: string = "";
  lastName: string = "";
}

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private _user: User = new User();

  private authSubscription: Subscription;

  constructor(private httpService: HttpService,
              private authService: AuthService) {
    console.log("Constructing user service");

    this.authSubscription = this.authService.authSubject.subscribe(
      authenticated => {
        if (authenticated) {
          this.fetchCurrentUser();
        } else {
          this.resetUser();
        }
      }
    );
  }

  get user() { return this._user; }

  set user(newUser: User) {
    console.log("Called set user()");
    this._user.email = newUser.email;
    this._user.firstName = newUser.firstName;
    this._user.lastName = newUser.lastName;
  }

  fetchCurrentUser() {
    this.httpService.get(USER_SELF_URL)
      .subscribe(
        (user: User) => {
          console.log("Successfully got user:")
          console.log(user);
          this.user = user;
        },
        error => {
          console.log("Failed to get user:")
          console.log(error);
        }
      );
  }

  resetUser() {
    console.log("Clearing user information");
    this.user = new User();
  }
}
