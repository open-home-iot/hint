import { Component, OnInit } from '@angular/core';
import {EventHandlerService} from "./events/event-handler.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Longest web app title in the fucking universe';

  constructor(private eventHandler: EventHandlerService) {
    eventHandler.events.subscribe(event => {
      console.log("Event received: " + event);
    });
  }

  ngOnInit(): void {
  }
}
