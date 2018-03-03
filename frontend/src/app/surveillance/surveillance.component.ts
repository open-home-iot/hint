import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Event, EventHandlerService} from "../events/event-handler.service";
import {ActivatedRoute, Router} from "@angular/router";
import {relative} from "path";

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

  constructor(private http: HttpClient,
              private eventHandler: EventHandlerService,
              private router: Router,
              private route: ActivatedRoute) {
    eventHandler.events.subscribe(event => {
      this.newPicture(event);
    });
  }

  ngOnInit() {
    this.http.get<Pictures>(
      'http://' + window.location.hostname + ':8000/surveillance/pictures/'
    ).subscribe(
      data => {
        console.log(data);
        this.pictures = data.pictures;
      }
    );
  }

  newPicture(event: Event) {
    if (event.type === 'event.alarm' && event.content === 'on') {
      setTimeout(this.http.get<Pictures>(
        'http://' + window.location.hostname + ':8000/surveillance/pictures/'
      ).subscribe(
        data => {
          console.log(data);
          this.pictures = data.pictures;
        }), 1000);
    }
  }

  enlargePicture(picture: string) {
    this.router.navigate(['picture', picture], {
      relativeTo: this.route
    });
  }

}
