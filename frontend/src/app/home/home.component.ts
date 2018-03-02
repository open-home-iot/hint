import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {EventHandlerService, Event, EventStatus} from "../events/event-handler.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: []
})
export class HomeComponent implements OnInit {
  info: any;
  alarmIndication: boolean;

  constructor(private http: HttpClient, private eventHandler: EventHandlerService) {
    eventHandler.events.subscribe(event => {
      this.updateAlarmStatus(event);
    });
  }

  ngOnInit() {
    const header: HttpHeaders = new HttpHeaders().set('Authorization', 'Basic ' + btoa('mth:password123'));

    this.http.get(
      window.location.protocol + '//' + window.location.hostname + ':8000' + '/api/info/',
      { headers: header }
    ).subscribe(
      data => {
        console.log(data);
        this.info = data;
      },
      err => {
        console.log(err);
      });

    this.http.get<EventStatus>(
      window.location.protocol + '//' + window.location.hostname + ':8000' + '/events/status',
      { headers: header }
    ).subscribe(
      data => {
        console.log(data);
        this.alarmIndication = data.alarm;
      },
      err => {
        console.log(err);
      });
  }

  updateAlarmStatus(event: Event) {
    this.alarmIndication = event.content !== 'off';
  }
}
