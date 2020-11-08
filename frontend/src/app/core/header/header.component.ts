import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {
  authenticated: boolean = false;

  private authSubscription: Subscription;

  constructor(private authService: AuthService) { }

  ngOnInit() {
    this.authSubscription = this.authService.authSubject.subscribe(
      next => {
        this.authenticated = next;
      }
    );
  }

  showLogin(){
    console.log("test");
    document.querySelector("#auth-login").classList.remove("hidden");
  }

  ngOnDestroy() {
    this.authSubscription.unsubscribe();
  }


}
