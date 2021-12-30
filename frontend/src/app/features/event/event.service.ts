import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';
import {idGenerator} from '../../core/utility';

export interface HumeEvent {
  hume_uuid: string;
  event_type: number;
  content: any;
}

interface Subscription {
  hume_uuid: string;
  event_type: number;
  callback: (event) => void;
}

export const ALL_HUMES = "*"

// event types
export const HUB_DISCOVER_DEVICES = 0;
export const DEVICE_ATTACHED = 1;

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap = new Map<number, Subscription>();
  private idGenerator = idGenerator();

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event: HumeEvent) {
    this.subscriptionMap.forEach(
      (subscription: Subscription, _) => {
        if (subscription.hume_uuid === event.hume_uuid ||
          subscription.hume_uuid === ALL_HUMES) {
          if (subscription.event_type === event.event_type) {
            subscription.callback(event);
          }
        }
      }
    );
  }

  /**
   * Subscribe to an event type from a HUME, or all HUMEs (use the ALL_HUMES
   * const).
   *
   * @param humeUUID
   * @param eventType
   * @param callback
   */
  subscribe(humeUUID: string,
            eventType: number,
            callback: (event) => void): number {
    const SUBSCRIPTION_ID = Number(this.idGenerator.next().value);
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

  unsubscribe(subscriptionID: number) {
    this.subscriptionMap.delete(subscriptionID);
  }

  monitorHume(humeUUID: string) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({ hume_uuid: humeUUID }));
  }
}
