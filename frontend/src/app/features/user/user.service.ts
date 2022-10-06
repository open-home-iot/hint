import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Subscription } from 'rxjs';

import { AuthService } from '../../core/auth/auth.service';

const USER_SELF_URL = window.location.origin + '/api/users/self';

export interface User {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private user: User;
  private authSubscription: Subscription;

  constructor(private httpClient: HttpClient,
              private authService: AuthService) {
    this.authSubscription = this.authService.authSubject.subscribe(
      authenticated => {
        if (authenticated) {
          this.getUser()
            .then((user: User) => {
              this.user = user;
            })
            .catch(error => {
              console.error(error);
            });
        } else {
          this.resetUser();
        }
      }
    );
  }

  getUser(): Promise<User> {
    if (this.user) {
      return Promise.resolve(this.user);
    }

    return new Promise<User>((resolve, reject) => {
      this.httpClient.get(USER_SELF_URL)
        .subscribe(
          (user: User) => {
            this.user = user;
            resolve(this.user);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  resetUser(): void {
    this.user = undefined;
  }

  updateUser(user: User) {
    return this.httpClient.put(USER_SELF_URL, user);
  }
}
