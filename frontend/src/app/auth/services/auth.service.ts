import { Injectable } from '@angular/core';

import { BehaviorSubject } from 'rxjs/BehaviorSubject';

import { RequestService } from '../../api-interface/request.service';


const BASE_URL = window.location.protocol + '//' + window.location.hostname + ':8000/api/';
const LOGIN_URL = BASE_URL + 'login/';
const LOGOUT_URL = BASE_URL + 'logout/';


@Injectable()
export class AuthService {
  // The subject contains the current authentication state of the user. BehaviorSubjects when subscribed to will emit
  // its latest value.
  authSubject: BehaviorSubject<boolean>;

  constructor(private requestService: RequestService) {
    this.authSubject = new BehaviorSubject<boolean>(false);
  }

  login(username: string, password: string) {
    this.requestService.post(LOGIN_URL, { username: username, password: password })
      .subscribe(
        next => {
          this.authSubject.next(true);
          console.log("[AuthService] Success logging in.");
        });
  }

  logout() {
    this.requestService.post(LOGOUT_URL, {})
    .subscribe(
      next => {
        this.authSubject.next(false);
        console.log('[AuthService] Success logging out.');
      });
  }

  isAuthenticated(): Promise<boolean> {
    return new Promise<boolean>(
      (resolve, reject) => {
        this.requestService.post(LOGIN_URL, { username: '', password: '' })
          .subscribe(
            next => {
              resolve(true);
            },
            error => {
              resolve(false);
            }
          );
      }
    );
  }
}
