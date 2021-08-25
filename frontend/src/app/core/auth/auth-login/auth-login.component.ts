import { Component, OnDestroy, OnInit} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { AuthService } from '../auth.service';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';


@Component({
  selector: 'app-auth-login',
  templateUrl: './auth-login.component.html',
  styleUrls: ['./auth-login.component.scss']
})
export class AuthLoginComponent implements OnInit, OnDestroy {
  apiLoginError = false;
  apiLoginErrorMessages: [] = [];

  loginForm: FormGroup;

  private authSubscription: Subscription;

  constructor(private authService: AuthService,
              private formBuilder: FormBuilder,
              private router: Router) { }

  ngOnInit() {
    this.authSubscription = this.authService.authSubject.subscribe(
      authenticated => {
        if (authenticated) {
          this.router.navigate(['/']);
        }
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
        this.router.navigate(['/']);
      },
      (error: HttpErrorResponse) => {
        console.error('Manual login failed!');
        this.apiLoginError = true;
        this.apiLoginErrorMessages = Object.assign([], error.error.auth);
      });
  }
}
