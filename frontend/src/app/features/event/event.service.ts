import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';


class HomeEvent {
  homeId: number;
  humeUUID: string;
  deviceUUID: string;
}

@Injectable()
export class EventService {

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event: HomeEvent) {
    console.log(event);

    // TODO add subscription function for hub/device specific events. When
    // onEvent is called, parse current component subscriptions and notify
  }

  subscribeToHumeEvents(humeUUID: string, callback: Function) {
    console.log("Subscribing to hume events: " + humeUUID);
  }

  subscribeToDeviceEvents(deviceUUID: string, callback: Function) {
    console.log("Subscribing to device events: " + deviceUUID);
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({"home_id": homeId}));
  }
}
