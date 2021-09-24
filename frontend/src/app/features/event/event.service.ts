import { Injectable } from '@angular/core';

import { Utility } from '../../core/utility';
import { WebSocketService } from '../../core/websocket/websocket.service';


export interface HumeEvent {
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

  onEvent(event: HumeEvent) {
    this.subscriptionMap.forEach(
      (subscription: Subscription, _) => {
        if (subscription.hume_uuid === event.hume_uuid) {

          if (subscription.event_type === event.event_type) {
            subscription.callback(event);
          }
        }
      }
    );
  }

  subscribe(humeUUID: string,
            eventType: number,
            callback: (event) => void): string {
    // TODO: oh my god replace this crap with an auto-incrementing number...
    const SUBSCRIPTION_ID = Utility.generateRandomID();

    if (this.subscriptionMap.has(SUBSCRIPTION_ID)) {
      throw new Error('Input subscriptionID already taken');
    }

    this.subscriptionMap.set(
      SUBSCRIPTION_ID,
      {
        hume_uuid:  humeUUID,
        event_type: eventType,
        callback,
      }
    );

    return SUBSCRIPTION_ID;
  }

  unsubscribe(subscriptionID: string) {
    this.subscriptionMap.delete(subscriptionID);
  }

  monitorHume(humeUUID: string) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({ hume_uuid: humeUUID }));
  }
}
