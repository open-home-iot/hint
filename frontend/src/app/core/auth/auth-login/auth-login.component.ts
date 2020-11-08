import { Component, OnDestroy, OnInit} from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { AuthService } from '../auth.service'
import { Subscription } from 'rxjs';
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';


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
    this.authService.loginWithPromise(this.email.value, this.password.value)
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


@Component({
  selector: 'ngbd-modal-basic',
  templateUrl: './auth-login.modal.html'
})
export class NgbdModalBasic {
  closeResult = '';

  constructor(private modalService: NgbModal) {}

  open(content) {
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }
}

