import { Component, OnDestroy, OnInit} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { AuthService } from '../auth.service'
import { Subscription } from 'rxjs';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-auth-login',
  templateUrl: './auth-login.component.html',
  styleUrls: ['./auth-login.component.scss']
})
export class AuthLoginComponent implements OnInit, OnDestroy {
  authenticated: boolean;

  apiLoginError: boolean = false;
  apiLoginErrorMessages: [] = [];
  apiLoginSuccess: boolean = false;

  loginForm: FormGroup;

  private authSubscription: Subscription;

  constructor(private authService: AuthService,
              private formBuilder: FormBuilder,
              private modalService: NgbModal) { }

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
    this.authService.loginWithPromise(this.email.value, this.password.value)
      .then(() => {
        this.apiLoginError = false;
        this.apiLoginSuccess = true;
      },
      (error: HttpErrorResponse) => {
        console.error("Manual login failed!")
        this.apiLoginError = true;
        this.apiLoginErrorMessages = Object.assign([], error.error.auth);
      });
  }

  open(content) {
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'})
  };
}
