import { Component, OnInit } from '@angular/core';

import { EventService, HomeEvent } from '../../event.service';
import { HomeService, Home } from '../../../home/home.service';
import { HumeService, Hume } from '../../../hume/hume.service';
import { WebSocketService } from '../../../../core/websocket/websocket.service';

@Component({
  selector: 'app-event-overview',
  templateUrl: './event-overview.component.html',
  styleUrls: ['./event-overview.component.scss'],
  providers: [EventService]
})
export class EventOverviewComponent implements OnInit {

  events: HomeEvent[] = [];

  constructor(private eventService: EventService,
              private homeService: HomeService,
              private humeService: HumeService,
              private webSocketService: WebSocketService) { }

  ngOnInit() { }

  subscribe() {
    let homes = this.homeService.homes;
    for (let home of homes) {
      this.eventService.subscribeToHomeEvents(home.id, this.onEvent.bind(this));
      let humes = this.humeService.getHomeHumes(home.id);
      for (let hume of humes) {
        this.eventService.subscribeToHumeEvents(hume.uuid, this.onEvent.bind(this));
      }
    }
  }

  test() {
    let homes = this.homeService.homes;
    for (let home of homes) {
      let humes = this.humeService.getHomeHumes(home.id);
      for (let hume of humes) {
        this.webSocketService.send(JSON.stringify({"testing": 1,
                                                   "home_id": home.id,
                                                   "hume_uuid": hume.uuid}));
      }
    }
  }

  onEvent(event: HomeEvent) {
    console.log(event);
    this.events.push(event);
  }
}
