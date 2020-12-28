import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';


export class HomeEvent {
  home_id: number;
  hume_uuid: string;
  device_uuid: string;
}

interface SubscriptionKey {
  homeId: number;
  humeUUID: string;
  deviceUUID: string;
}

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap: {
    (subscriptionKey: keyof SubscriptionKey): Function[]
  } | {} = {};

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event: string) {
    let decoded_event: HomeEvent = JSON.parse(event);
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

  subscribeToHomeEvents(homeId: number, callback: Function) {
    console.log("Subscribing to home events: " + String(homeId));
    if (!(homeId in this.subscriptionMap)) {
      this.subscriptionMap[homeId] = [];
    }

    this.subscriptionMap[homeId].push(callback);
    console.log(this.subscriptionMap)
  }

  subscribeToHumeEvents(humeUUID: string, callback: Function) {
    console.log("Subscribing to hume events: " + humeUUID);
    if (!(humeUUID in this.subscriptionMap)) {
      this.subscriptionMap[humeUUID] = [];
    }

    this.subscriptionMap[humeUUID].push(callback);
    console.log(this.subscriptionMap)
  }

  subscribeToDeviceEvents(deviceUUID: string, callback: Function) {
    console.log("Subscribing to device events: " + deviceUUID);
    if (!(deviceUUID in this.subscriptionMap)) {
      this.subscriptionMap[deviceUUID] = [];
    }

    this.subscriptionMap[deviceUUID].push(callback);
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({"home_id": homeId}));
  }
}
