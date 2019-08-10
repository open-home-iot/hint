import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpService } from '../http/http.service';

const LOGIN_URL = window.location.href + "api/user/login";
const LOGOUT_URL = window.location.href + "api/user/logout";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  authSubject: BehaviorSubject<boolean>;

  constructor(private httpService: HttpService) {
    this.authSubject = new BehaviorSubject<boolean>(false);
    this.login("", "");
  }

  login(username: string, password: string) {
    this.httpService.post(LOGIN_URL, { username: username, password: password })
      .subscribe(
      next => {
          console.log("Success logging in!");
          this.authSubject.next(true);
        }
      );
  }

  logout() {
    this.httpService.post(LOGOUT_URL, {})
      .subscribe(
        next => {
          console.log("Success logging out!");
          this.authSubject.next(false);
        }
      );
  }

  isAuthenticated(): Promise<boolean> {
    return new Promise<boolean>(
      (resolve, reject) => {
        this.httpService.post(LOGIN_URL, { username: '', password: '' })
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
