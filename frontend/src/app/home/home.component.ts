import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  info: any;

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.http.get(
      'http://localhost:8000/api/info/',
      { headers: new HttpHeaders().set('Authorization', 'Basic ' + btoa('admin:Horseseathay1')) }
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
