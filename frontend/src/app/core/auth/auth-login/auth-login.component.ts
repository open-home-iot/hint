import { Component, OnDestroy, OnInit} from '@angular/core';
import { NgForm} from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { AuthService } from '../auth.service'
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-auth-login',
  templateUrl: './auth-login.component.html',
  styleUrls: ['./auth-login.component.scss']
})
export class AuthLoginComponent implements OnInit, OnDestroy {
  authenticated: boolean;

  apiLoginError: boolean = false;
  apiLoginErrorMessages: [] = [];

  private authSubscription: Subscription;

  constructor(private authService: AuthService) { }

  ngOnInit() {
    this.authSubscription = this.authService.authSubject.subscribe(
      next => {
        this.authenticated = next;
      }
    );
  }

  ngOnDestroy() {
    this.authSubscription.unsubscribe();
  }

  login(form: NgForm) {
    const username = form.value.username;
    const password = form.value.password;

    this.authService.loginWithPromise(username, password)
      .then(() => {
        console.log("Manual login succeeded!");
        this.apiLoginError = false;
      },
      (error: HttpErrorResponse) => {
        console.log("Manual login failed!")
        this.apiLoginError = true;
        this.apiLoginErrorMessages = Object.assign([], error.error.auth);
      });
  }
}
