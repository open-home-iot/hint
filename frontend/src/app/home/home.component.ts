import { Component, OnInit } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';

import { EventHandlerService, Event } from '../events/services/event-handler.service';
import { RequestService } from '../api-interface/request.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: []
})
export class HomeComponent implements OnInit {
  info: any;
  alarmIndication: boolean;

  constructor(private eventHandler: EventHandlerService,
              private requestService: RequestService) {
    eventHandler.events.subscribe(event => {
      this.updateAlarmStatus(event);
    });
  }

  ngOnInit() {
    const header: HttpHeaders = new HttpHeaders().set('Authorization', 'Basic ' + btoa('mth:password123'));

    this.requestService.get('http://' + window.location.hostname + ':8000/api/info/', {})
      .subscribe(
      data => {
        this.info = data.results;
      });

    this.requestService.get('http://' + window.location.hostname + ':8000/api/events/status', {})
      .subscribe(
      data => {
        this.alarmIndication = data.results[0];
      });
  }

  updateAlarmStatus(event: Event) {
    this.alarmIndication = event.content !== 'off';
  }
}
