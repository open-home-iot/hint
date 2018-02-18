import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {EventListenerService} from "../events/event-listener.service";
import {EventHandlerService} from "../events/event-handler.service";

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
      console.log("Got an event type: " + event.type + "\nwith content: " + event.content);
    });
  }

  ngOnInit() {
    this.http.get(
      'http://localhost:8000/api/info/',
      { headers: new HttpHeaders().set('Authorization', 'Basic ' + btoa('mth:password123')) }
    ).subscribe(
      data => {
        console.log(data);
        this.info = data;
      },
      err => {
        console.log(err);
      });
  }

  getAlarmIndication() {
    this.eventHandler.events.next({
      type: 'events.alarm',
      content: 'ok'
    });
  }
}
