import { Injectable } from '@angular/core';


const WS_BASE_URL = window.location.origin;


@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  private ws: WebSocket;
  private callback: any;
  private messageBuffer: {"home_id": number}[] = [];

  constructor() {
    this.ws = new WebSocket(
      WS_BASE_URL.replace("http://", "ws://")
    );
    this.ws.onopen = this.onSocketOpen.bind(this);
    this.ws.onclose = this.onSocketClose.bind(this);
    this.ws.onerror = this.onSocketError.bind(this);
    this.ws.onmessage = this.onSocketMessage.bind(this);
  }

  private onSocketOpen(event: Event) {
    console.log(event);
    while (this.messageBuffer.length > 0) {
      this.send(this.messageBuffer.pop());
    }
  }

  private onSocketClose(event: CloseEvent) {
    console.log(event);
  }

  private onSocketError(event: Event) {
    console.error(event);
  }

  private onSocketMessage(event: MessageEvent) {
    console.log(event);
    this.callback(event.data);
  }

  registerCallback(callback) {
    this.callback = callback;
  }

  send(message) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      this.messageBuffer.push(message);
    }
  }
}
