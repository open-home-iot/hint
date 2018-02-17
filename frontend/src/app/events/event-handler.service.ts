import { Injectable } from '@angular/core';

import { EventListenerService } from "./event-listener.service";
import { Subject } from "rxjs/Subject";


const WS_URL = 'ws://localhost:8000';

export interface Event {
  type: number,
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
          type: event.type
        }
      });
  }
}
