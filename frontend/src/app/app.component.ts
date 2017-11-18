import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'app';
  users: any;
  groups: any;
  info: any;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const headers = new HttpHeaders().set('Authorization', 'Basic ' + btoa('admin:Horseseathay1'))
    // btoa() needs to be used since the Authorization header uses base64 encoding!
    // Without it, the request will fail with error code 401, unauthorized since it
    // cannot decode the request header.
    this.http.get(
      'http://localhost:8000/api/users/',
      { headers: headers }
      ).subscribe(
        data => {
          console.log(data);
          this.users = data;
      },
        err => {
          console.log(err);
    });

    this.http.get(
      'http://localhost:8000/api/groups/',
      { headers: headers }
      ).subscribe(
        data => {
          console.log(data);
          this.groups = data;
      },
        err => {
          console.log(err);
    });

    this.http.get(
      'http://localhost:8000/api/info/',
      { headers: headers }
      ).subscribe(
        data => {
          console.log(data);
          this.info = data;
      },
        err => {
          console.log(err);
    });

  }
}
