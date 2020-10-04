import { Component, OnInit } from '@angular/core';
import { NgForm} from '@angular/forms';

import { HttpService } from '../../http/http.service';

const SIGN_UP_URL = window.location.origin + "/api/user/sign-up"

@Component({
  selector: 'app-auth-sign-up',
  templateUrl: './auth-sign-up.component.html',
  styleUrls: ['./auth-sign-up.component.scss']
})
export class AuthSignUpComponent implements OnInit {

  constructor(private httpService: HttpService) { }

  ngOnInit() {
  }

  signUp(form: NgForm) {
    console.log(window.location.origin);

    const email = form.value.email;
    const firstName = form.value.first_name;
    const lastName = form.value.last_name;
    const password = form.value.password;
    const confirm_password = form.value.confirm_password;

    console.log("Email: " + email);
    console.log("First name: " + firstName);
    console.log("Last name: " + lastName);
    console.log("Password: " + password);
    console.log("Confirm password: " + confirm_password);

    this.httpService.post(
      SIGN_UP_URL,
      { email: email, first_name: firstName, last_name: lastName,
        password: password })
        .subscribe(
          next => {
            console.log("Sign up successful!");
          },
          error => {
            console.log("Sign up failed!");
          }
        );
  }
}
