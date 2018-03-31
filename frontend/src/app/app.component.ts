import { Component, OnInit } from '@angular/core';

import { AuthService } from './auth/services/auth.service';
import { RequestService } from './api-interface/request.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Longest web app title in the fucking universe';
  django_img_path = 'http://' + window.location.hostname + ':8000' + '/static/images/django_logo.png';
  angular_img_path = 'http://' + window.location.hostname + ':8000' + '/static/images/angular_whiteTransparent.png';

  constructor(private requestService: RequestService,
              private authService: AuthService) {}

  ngOnInit() {
    this.requestService.get('http://localhost:8000/api/csrf/')
      .subscribe(
        next => {
          this.authService.login('', '');
        }
    );
  }
}
