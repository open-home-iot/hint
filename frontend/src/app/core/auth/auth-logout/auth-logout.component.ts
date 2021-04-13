import { Component, OnDestroy, OnInit} from '@angular/core';

import { AuthService } from '../auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-auth-logout',
  templateUrl: './auth-logout.component.html',
  styleUrls: ['./auth-logout.component.scss']
})
export class AuthLogoutComponent implements OnInit, OnDestroy {
  authenticated: boolean;

  private authSubscription: Subscription;

  constructor(private authService: AuthService) { }

  ngOnInit() {
    this.authSubscription = this.authService.authSubject.subscribe(
      next => {
        this.authenticated = next;
      }
    );
  }

  ngOnDestroy() {
    this.authSubscription.unsubscribe();
  }

  logout() {
    this.authService.logout();
  }
}
