import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

import { HttpService } from '../../http/http.service';

import { passwordValidator } from '../../directives/validators/confirm-password.directive';

const SIGN_UP_URL = window.location.origin + "/api/user/sign-up"

@Component({
  selector: 'app-auth-sign-up',
  templateUrl: './auth-sign-up.component.html',
  styleUrls: ['./auth-sign-up.component.scss']
})
export class AuthSignUpComponent implements OnInit {

  signUpForm: FormGroup;
  apiEmailError: boolean = false;
  apiEmailErrorMessages: [] = [];

  constructor(private router: Router,
              private httpService: HttpService,
              private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.signUpForm = this.formBuilder.group({
      auth: this.formBuilder.group({
        email: ['', Validators.required],
        password: ['', Validators.required],
        confirmPassword: ['', Validators.required]
      }),
      personalInfo: this.formBuilder.group({
        firstName: [''],
        lastName: ['']
      })
    },
    { validators: passwordValidator });
  }

  get email() { return this.signUpForm.get('auth.email'); }
  get password() { return this.signUpForm.get('auth.password'); }
  get confirmPassword() { return this.signUpForm.get('auth.confirmPassword'); }
  get firstName() { return this.signUpForm.get('personalInfo.firstName'); }
  get lastName() { return this.signUpForm.get('personalInfo.lastName'); }

  signUp() {
    console.log(this.signUpForm.value);

    this.httpService.post(
      SIGN_UP_URL,
      { email: this.email.value,
        first_name: this.firstName.value,
        last_name: this.lastName.value,
        password: this.password.value
      })
      .subscribe(
        response => {
          console.log("Sign up succeeded!");
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
