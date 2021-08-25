import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { BehaviorSubject } from 'rxjs';

const LOGIN_URL = window.location.origin + '/api/users/login';
const LOGOUT_URL = window.location.origin + '/api/users/logout';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  authSubject = new BehaviorSubject<boolean>(false);

  // Has it been confirmed that the authSubject is aligned with the backend
  // authentication status?
  private initiated = false;

  constructor(private httpClient: HttpClient,
              private router: Router) {
    console.log("Constructing AuthService");
    // Initial login attempt to check if the user is authenticated. This works
    // without username/password since the CSRF token cookie works as an
    // identifier for the session that the user was given upon his/her last
    // login. And the CSRF token cookie always gets set on outgoing HTTP
    // requests, see the AuthInterceptor for more information.
    this.login('', '');
  }

  login(username: string, password: string) {
    this.httpClient.post(LOGIN_URL, { username, password })
      .subscribe(
        _ => {
          this.updateAuthService(true);
        },
        (error: HttpErrorResponse) => {
          console.error(error);
          this.updateAuthService(false);
        }
    );
  }

  loginWithPromise(username: string, password: string) {
    return new Promise<void>((resolve, reject) => {
      this.httpClient.post(LOGIN_URL, { username, password })
        .subscribe(
          next => {
            this.updateAuthService(true);
            resolve();
          },
          (error: HttpErrorResponse) => {
            console.error(error);
            this.updateAuthService(false);
            reject(error);
          }
        );
    });
  }

  logout() {
    this.httpClient.post(LOGOUT_URL, {})
      .subscribe(
        next => {
          this.updateAuthService(false);
          this.router.navigate(['/']);
        },
        error => {
          console.error(error);
        }
      );
  }

  /**
   *
   */
  isAuthenticated(): Promise<boolean> {
    return new Promise<boolean>(
      (resolve, reject) => {
        // If the AuthService has been initiated, then the value held by the authSubject is correct.
        if (this.initiated) {
          resolve(this.authSubject.getValue());
          // If not, we need to wait for the AuthService to initiate.
        } else {
          this.authSubject.subscribe(
            next => {
              if (this.initiated) {
                resolve(this.authSubject.getValue());
              }
            }
          );
        }
      }
    );
  }

  updateAuthService(newState: boolean) {
    this.initiated = true; // As the authSubject is updated, we now set the AuthService state to "initiated".
    this.authSubject.next(newState);
  }
}
