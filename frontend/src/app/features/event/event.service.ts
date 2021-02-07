import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';

export class HomeEvent {
  home_id: number;
  hume_uuid: string;
  device_uuid: string;
  content: any;
}

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap: {
    (subscriptionKey: (number | string)): Function[]
  } | {} = {};

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event: string) {
    let decoded_event: HomeEvent = JSON.parse(event);
    console.log("onEvent ")
    console.log(decoded_event);

    if (decoded_event.home_id in this.subscriptionMap) {
      for (let callback of this.subscriptionMap[decoded_event.home_id]) {
        callback(decoded_event)
      }
    }
    if (decoded_event.hume_uuid in this.subscriptionMap) {
      for (let callback of this.subscriptionMap[decoded_event.hume_uuid]) {
        callback(decoded_event)
      }
    }
    if (decoded_event.device_uuid in this.subscriptionMap) {
      for (let callback of this.subscriptionMap[decoded_event.device_uuid]) {
        callback(decoded_event)
      }
    }
  }

  subscribe(subscriptionKey: number | string, callback: Function) {
    console.log("Subscribing to key: " + String(subscriptionKey));
    if (!(subscriptionKey in this.subscriptionMap)) {
      this.subscriptionMap[subscriptionKey] = [];
    }
    console.log("in event service " + this.subscriptionMap[subscriptionKey]);
    this.subscriptionMap[subscriptionKey].push(callback);
    console.log(this.subscriptionMap)
  }

  unsubscribe(subscriptionKey: number | string) {
    console.log(this.subscriptionMap);
    delete this.subscriptionMap[subscriptionKey];
    console.log(this.subscriptionMap);
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({"home_id": homeId}));
  }
}
