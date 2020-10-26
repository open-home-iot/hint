import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';

@Injectable()
export class EventService {

  constructor(private webSocketService: WebSocketService) { }

  subscribe(callback) {
    this.webSocketService.subscribe(callback);
  }

  send(message) {
    this.webSocketService.send(message);
  }
}
