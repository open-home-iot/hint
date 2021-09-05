import { Component, OnInit } from '@angular/core';

import { UserService, User } from '../../user.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import { PASSWORD_VALIDATOR } from '../../../../core/directives/validators/confirm-password.directive';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import {AuthService} from '../../../../core/auth/auth.service';
import {ValueConverter} from '@angular/compiler/src/render3/view/template';

const DEFAULT_FIRST_NAME = 'Mr.';
const DEFAULT_LAST_NAME = 'Andersson';

@Component({
  selector: 'app-user-overview',
  templateUrl: './user-overview.component.html',
  styleUrls: ['./user-overview.component.scss']
})
export class UserOverviewComponent implements OnInit {

  user: User;

  changeName: boolean = false;
  firstNameLength = 1;
  lastNameLength = 1;

  nameForm: FormGroup
  emailForm: FormGroup;
  authForm: FormGroup;

  apiEmailErrorMessages: string[] = [];

  constructor(private userService: UserService,
              private authService: AuthService,
              private httpClient: HttpClient,
              private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.userService.getUser()
      .then(this.onGetUser.bind(this))
      .catch(this.onGetUserFailed);

    this.emailForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
    });

    this.authForm = this.formBuilder.group({
      auth: this.formBuilder.group({
          password:        ['', Validators.required],
          confirmPassword: ['', Validators.required]
      })
    },
    { validators: PASSWORD_VALIDATOR });

    this.nameForm = this.formBuilder.group({
      firstName: ['', [Validators.required, Validators.maxLength(50)]],
      lastName: ['', [Validators.required, Validators.maxLength(50)]],
    });
  }

  get email() { return this.emailForm.get('email'); }
  get password() { return this.authForm.get('auth.password'); }
  get confirmPassword() { return this.authForm.get('auth.confirmPassword'); }
  get firstName() { return this.nameForm.get('firstName') }
  get lastName() { return this.nameForm.get('lastName') }

  firstNameChange() {
    if (this.firstName.value.length !== 0 ) {
      this.firstNameLength = this.firstName.value.length;
    } else {
      this.firstNameLength = 1;
    }
  }

  lastNameChange() {
    if (this.lastName.value.length !== 0) {
      this.lastNameLength = this.lastName.value.length;
    } else {
      this.lastNameLength = 1;
    }
  }

  nameSubmit() {
    this.userService.updateUser(
      <User>{first_name: this.firstName.value, last_name: this.lastName.value}
    ).subscribe(
      _ => {
        this.changeName = false;
        this.user.first_name = this.firstName.value;
        this.user.last_name = this.lastName.value;
      },
      error => {
        console.error(error);
      },
    );
  }

  emailSubmit() {
    this.userService.updateUser(
      <User>{email: this.email.value}
    ).subscribe(
      _ => {
        this.apiEmailErrorMessages.length = 0;
        this.user.email = this.email.value;
      },
      (error: HttpErrorResponse) => {
        if (error.error.email) {
            this.apiEmailErrorMessages = Object.assign([], error.error.email);
          } else {
            this.apiEmailErrorMessages.length = 0;
            this.apiEmailErrorMessages.push('Could not update email address.');
          }
        }
    );
  }

  authSubmit() {
    this.userService.updateUser(
      <User>{password: this.password.value}
    ).subscribe(
      _ => {
        this.authService.loginWithPromise(this.user.email, this.password.value)
          .then(_ => {
            this.authForm.reset();
          })
          .catch(error => {
            console.log(error);
          });
      },
      error => { console.error(error); }
    );
  }

  private onGetUser(user: User): void {
    this.user = user;
    this.email.setValue(user.email);

    if (this.user.first_name === '') {
      this.user.first_name = DEFAULT_FIRST_NAME;
    }
    if (this.user.last_name === '') {
      this.user.last_name = DEFAULT_LAST_NAME;
    }
    this.nameForm.patchValue(
      {firstName: this.user.first_name, lastName: this.user.last_name},
    );
    this.firstNameChange();
    this.lastNameChange();
  }

  private onGetUserFailed(error) {
    console.error(error);
  }
}
