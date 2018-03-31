import { Injectable } from '@angular/core';

import { EventListenerService } from './event-listener.service';
import { Subject } from 'rxjs/Subject';

/*
The echo URL is a way to verify that websocket messages are actually sent out and received as they should be.
 */

//const WS_URL = 'ws://echo.websocket.org/';
// Add whatever ws address should be used.
const WS_URL = 'ws://' + window.location.hostname + ':8000/';

export interface Event {
  type: string,
  content: string
}


@Injectable()
export class EventHandlerService {
  public events : Subject<Event>;

  constructor(eventListener: EventListenerService) {
    this.events = <Subject<Event>>eventListener
      .connect(WS_URL)
      .map((response: MessageEvent): Event => {
        let event = JSON.parse(response.data);
        return {
          type: event.type,
          content: event.content
        }
      });
  }
}
