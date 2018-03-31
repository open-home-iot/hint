import { Component, OnInit } from '@angular/core';
import {EventHandlerService} from "./events/services/event-handler.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Longest web app title in the fucking universe';
  django_img_path = 'http://' + window.location.hostname + ':8000' + '/static/images/django_logo.png';
  angular_img_path = 'http://' + window.location.hostname + ':8000' + '/static/images/angular_whiteTransparent.png';

  constructor(private eventHandler: EventHandlerService) {
    eventHandler.events.subscribe(event => {
      console.log("Event received: " + event);
    });
  }

  ngOnInit(): void {
  }
}
