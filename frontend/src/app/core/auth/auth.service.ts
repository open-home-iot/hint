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
  authSubject: BehaviorSubject<boolean>;

  private initiated: boolean; // Indicates if the AuthService has up-to-date information.

  constructor(private httpClient: HttpClient,
              private router: Router) {
    this.initiated = false; // Initially, we do not have up-to-date information.
    this.authSubject = new BehaviorSubject<boolean>(false);

    // Initial login attempt to check if the user is authenticated. This works
    // without username/password since the CSRF token cookie works as an
    // identifier for the session that the user was given upon his/her last
    // login. And the CSRF token cookie always gets set on outgoing HTTP
    // requests, see the AuthInterceptor for more information.
    this.login('', '');
  }

  sendLoginRequest(username: string, password: string) {
    return this.httpClient.post(LOGIN_URL, { username, password });

  }

  login(username: string, password: string) {
    const OBS = this.sendLoginRequest(username, password);

    OBS.subscribe(
      next => {
        this.updateAuthService(true);
      },
      (error: HttpErrorResponse) => {
        console.log('Failed to log in');
        console.log(error);
        this.updateAuthService(false);
      }
    );
  }

  loginWithPromise(username: string, password: string) {
    return new Promise<void>((resolve, reject) => {
      this.sendLoginRequest(username, password)
        .subscribe(
          next => {
            this.updateAuthService(true);
            resolve();
          },
          (error: HttpErrorResponse) => {
            console.log('Failed to log in');
            console.log(error);
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
          console.log('Success logging out!');
          this.updateAuthService(false);
          this.router.navigate(['/']);
        },
        error => {
          console.log('Failed to log out');
          this.updateAuthService(false);
          this.router.navigate(['/']);
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
