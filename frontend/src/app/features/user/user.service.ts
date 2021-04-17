import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Subscription } from 'rxjs';

import { AuthService } from '../../core/auth/auth.service';

const USER_SELF_URL = window.location.origin + '/api/users/self';

export interface User {
  email: string;
  firstName: string;
  lastName: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;

  private authSubscription: Subscription;

  constructor(private httpClient: HttpClient,
              private authService: AuthService) {
    console.log('Constructing user service');

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

  fetchCurrentUser() {
    this.httpClient.get(USER_SELF_URL)
      .subscribe(
        (gottenUser: User) => {
          console.log('Successfully got user:');
          console.log(gottenUser);
          this.user = gottenUser;
        },
        error => {
          console.log('Failed to get user:');
          console.log(error);
        }
      );
  }

  resetUser() {
    console.log('Clearing user information');
    this.user = undefined;
  }
}
