import { Component, OnDestroy, OnInit} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
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

  get email() { return this.loginForm.get('email') }
  get password() { return this.loginForm.get('password') }

  login() {
    const email = this.email.value;
    const password = this.password.value;

    this.authService.loginWithPromise(email, password)
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
