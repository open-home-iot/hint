import { Component, OnInit } from '@angular/core';

import { EventService } from '../../event.service';

@Component({
  selector: 'app-event-overview',
  templateUrl: './event-overview.component.html',
  styleUrls: ['./event-overview.component.scss'],
  providers: [EventService]
})
export class EventOverviewComponent implements OnInit {

  msg: string = "";
  messages: string[];

  constructor(private eventService: EventService) { }

  ngOnInit() {
    this.messages = [];
  }

  onMessage(message: MessageEvent) {
    this.messages.push(message.data);
  }

  send() {
    this.eventService.send(this.msg);
  }
}
