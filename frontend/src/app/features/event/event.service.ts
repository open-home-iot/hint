import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';


export interface HumeEvent {
  home_id: number;
  hume_uuid: string;
  device_uuid: string;
  event_type: number;
  content: any;
}

interface Subscription {
  hume_uuid: string;
  event_type: number;
  callback: (event) => void;
}

export const HUB_DISCOVER_DEVICES = 0;

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap = new Map<string, Subscription>();

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event: string) {
    const DECODED_EVENT: HumeEvent = JSON.parse(event);

    this.subscriptionMap.forEach((subscription: Subscription, _) => {
      if(subscription.hume_uuid === DECODED_EVENT.hume_uuid) {

        if (subscription.event_type === DECODED_EVENT.event_type) {
          subscription.callback(DECODED_EVENT);
        }
      }
    });
  }

  subscribe(subscriptionId: string,
            humeUUID: string,
            eventType: number,
            callback: (event) => void) {
    console.log('Subscribing to key: ' + humeUUID);

    this.subscriptionMap[subscriptionId] = {
      hume_uuid: humeUUID,
      event_type: eventType,
      callback
    };
  }

  unsubscribe(subscriptionId: string) {
    delete this.subscriptionMap[subscriptionId];
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({home_id: homeId}));
  }
}
