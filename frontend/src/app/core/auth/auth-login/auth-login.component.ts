import { Component, OnDestroy, OnInit} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { AuthService } from '../auth.service';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-auth-login',
  templateUrl: './auth-login.component.html',
  styleUrls: ['./auth-login.component.scss']
})
export class AuthLoginComponent implements OnInit, OnDestroy {
  authenticated: boolean;

  apiLoginError = false;
  apiLoginErrorMessages: [] = [];
  apiLoginSuccess = false;

  loginForm: FormGroup;

  private authSubscription: Subscription;

  constructor(private authService: AuthService,
              private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.authSubscription = this.authService.authSubject.subscribe(
      next => {
        this.authenticated = next;
      }
    );

    this.loginForm = this.formBuilder.group({
      email: [''],
      password: ['']
    });
  }

  ngOnDestroy() {
    this.authSubscription.unsubscribe();
  }

  get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }

  login() {
    this.authService.loginWithPromise(this.email.value, this.password.value)
      .then(() => {
        this.apiLoginError = false;
        this.apiLoginSuccess = true;
      },
      (error: HttpErrorResponse) => {
        console.error('Manual login failed!');
        this.apiLoginError = true;
        this.apiLoginErrorMessages = Object.assign([], error.error.auth);
      });
  }
}
