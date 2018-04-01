import { Component, OnInit } from '@angular/core';

import { Event, EventHandlerService } from '../events/services/event-handler.service';
import { RequestService } from '../api-interface/request.service';


export interface Pictures {
  pictures: string[];
}

@Component({
  selector: 'app-surveillance',
  templateUrl: './surveillance.component.html',
  styleUrls: ['./surveillance.component.css']
})
export class SurveillanceComponent implements OnInit {
  pictures: string[];

  constructor(private requestService: RequestService,
              private eventHandler: EventHandlerService) {
    eventHandler.events.subscribe(event => {
      this.newPicture(event);
    });
  }

  ngOnInit() {
    this.requestService.get('http://' + window.location.hostname + ':8000/api/surveillance/pictures')
      .subscribe(
      data => {
        console.log(data);
        this.pictures = data.results;
      }
    );
  }

  newPicture(event: Event) {
    if (event.type === 'event.alarm' && event.content === 'on') {
      setTimeout(
        () => {
          this.requestService.get('http://' + window.location.hostname + ':8000/api/surveillance/pictures')
            .subscribe(
            data => {
              console.log(data);
              this.pictures = data.results;
        })
        }, 1000);
    }
  }
}
