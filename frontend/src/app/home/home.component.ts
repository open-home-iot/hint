import { Component, OnInit } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';

import { RequestService } from '../api-interface/request.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: []
})
export class HomeComponent implements OnInit {
  info: any;

  constructor(private requestService: RequestService) {
  }

  ngOnInit() {
    const header: HttpHeaders = new HttpHeaders().set('Authorization', 'Basic ' + btoa('mth:password123'));

    this.requestService.get('http://' + window.location.hostname + ':8000/api/info/', {})
      .subscribe(
      data => {
        this.info = data.results;
      });
  }
}
