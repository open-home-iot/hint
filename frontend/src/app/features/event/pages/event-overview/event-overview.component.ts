import { Component, OnInit, OnDestroy } from '@angular/core';

import { EventService, HomeEvent } from '../../event.service';
import { HomeService, Home } from '../../../home/home.service';
import { HumeService, Hume } from '../../../hume/hume.service';
import { WebSocketService } from '../../../../core/websocket/websocket.service';
import { HttpService } from '../../../../core/http/http.service';

@Component({
  selector: 'app-event-overview',
  templateUrl: './event-overview.component.html',
  styleUrls: ['./event-overview.component.scss'],
  providers: [EventService]
})
export class EventOverviewComponent implements OnInit, OnDestroy {

  events: HomeEvent[] = [];
  subscriptionKeys: (number | string)[] = []

  constructor(private eventService: EventService,
              private homeService: HomeService,
              private humeService: HumeService,
              private webSocketService: WebSocketService,
              private httpService: HttpService) { }

  ngOnInit() { }

  ngOnDestroy() {
    console.log("OnDestroy");
    console.log(this.subscriptionKeys)
    for (let key of this.subscriptionKeys) {
      this.eventService.unsubscribe(key);
    }
  }

  subscribe() {
    let homes = this.homeService.homes;
    for (let home of homes) {
      this.eventService.subscribe(home.id, this.onEvent.bind(this));
      this.subscriptionKeys.push(home.id);
      let humes = this.humeService.getHomeHumes(home.id);
      for (let hume of humes) {
        this.eventService.subscribe(hume.uuid, this.onEvent.bind(this));
        this.subscriptionKeys.push(hume.uuid);
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

  discoverDevicesTest() {
    this.httpService.get(
      window.location.origin + "/api/humes/98ab77d6-2cdb-11eb-b60d-60f81dbb505c/devices/discover"
    ).subscribe(
      success => {
        console.log(success);
      },
      error => {
        console.log(error)
      }
    );
  }

  onEvent(event: HomeEvent) {
    console.log(event);
    this.events.push(event);
  }
}
