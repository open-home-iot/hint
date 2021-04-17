import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

import { PASSWORD_VALIDATOR } from '../../directives/validators/confirm-password.directive';

const SIGN_UP_URL = window.location.origin + '/api/users/signup';

@Component({
  selector: 'app-auth-sign-up',
  templateUrl: './auth-sign-up.component.html',
  styleUrls: ['./auth-sign-up.component.scss']
})
export class AuthSignUpComponent implements OnInit {

  signUpForm: FormGroup;
  apiEmailError = false;
  apiEmailErrorMessages: [] = [];

  constructor(private router: Router,
              private httpClient: HttpClient,
              private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.signUpForm = this.formBuilder.group({
      auth: this.formBuilder.group({
        email: ['', Validators.required],
        password: ['', Validators.required],
        confirmPassword: ['', Validators.required]
      }),
      personalInfo: this.formBuilder.group({
        firstName: ['', Validators.maxLength(50)],
        lastName: ['', Validators.maxLength(50)]
      })
    },
    { validators: PASSWORD_VALIDATOR });
  }

  get email() { return this.signUpForm.get('auth.email'); }
  get password() { return this.signUpForm.get('auth.password'); }
  get confirmPassword() { return this.signUpForm.get('auth.confirmPassword'); }
  get firstName() { return this.signUpForm.get('personalInfo.firstName'); }
  get lastName() { return this.signUpForm.get('personalInfo.lastName'); }

  signUp() {
    console.log(this.signUpForm.value);

    this.httpClient.post(
      SIGN_UP_URL,
      { email: this.email.value,
        first_name: this.firstName.value,
        last_name: this.lastName.value,
        password: this.password.value
      })
      .subscribe(
        response => {
          console.log('Sign up succeeded!');
          this.router.navigate(['/']);
        },
        (error: HttpErrorResponse) => {
          this.apiEmailError = false;
          if (error.error.email) {
            this.apiEmailError = true;
            this.apiEmailErrorMessages = Object.assign([], error.error.email);
          }
        }
      );
  }
}
