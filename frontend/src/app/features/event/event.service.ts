import { Injectable } from '@angular/core';

import { WebSocketService, NOTIF_SOCKET_OPEN } from '../../core/websocket/websocket.service';
import { idGenerator } from '../../core/utility';

export interface HumeEvent {
  hume_uuid: string;
  device_uuid: string;
  event_type: number;
  content: any;
}

interface Subscription {
  hume_uuid: string;
  device_uuid: string;
  event_type: number;
  callback: (event) => void;
}

export const ALL_HUMES = '*';
export const NO_HUME_UUID = '';
export const NO_DEVICE_UUID = '';

// event types
export const HUB_DISCOVER_DEVICES = 0;
export const DEVICE_ATTACHED = 1;
export const STATEFUL_ACTION = 2;

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap = new Map<number, Subscription>();
  private idGenerator = idGenerator();
  private monitoredHumes: string[] = [];

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  /**
   * Subscribe to an event type from a HUME, or all HUMEs (use the ALL_HUMES
   * const).
   *
   * @param humeUUID
   * @param deviceUUID
   * @param eventType
   * @param callback
   */
  subscribe(humeUUID: string,
            deviceUUID: string,
            eventType: number,
            callback: (event) => void): number {
    const SUBSCRIPTION_ID = Number(this.idGenerator.next().value);
    this.subscriptionMap.set(
      SUBSCRIPTION_ID,
      {
        hume_uuid:  humeUUID,
        device_uuid: deviceUUID,
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
    this.monitoredHumes.push(humeUUID);
  }

  private onEvent(event: HumeEvent | string) {
    console.log(event);

    // Websocket has connected (or reconnected). Make sure we're subscribed
    // to HUME events.
    if (typeof event === 'string' || event instanceof String) {
      if (event === NOTIF_SOCKET_OPEN) {
        for (const HUME_UUID of this.monitoredHumes) {
          this.webSocketService.send(
            JSON.stringify({ hume_uuid: HUME_UUID})
          );
        }
      }
      return;
    }

    this.subscriptionMap.forEach(
      (subscription: Subscription, _) => {
        if (subscription.hume_uuid === event.hume_uuid ||
          subscription.hume_uuid === ALL_HUMES ||
          subscription.device_uuid === event.device_uuid) {
          if (subscription.event_type === event.event_type) {
            subscription.callback(event);
          }
        }
      }
    );
  }
}
