import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';

@Injectable()
export class EventService {

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event) {
    console.log(event);
  }

  send(message: {}) {
    this.webSocketService.send(message);
  }
}
