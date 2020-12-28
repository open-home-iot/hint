import { Injectable } from '@angular/core';


const WS_BASE_URL = window.location.origin;


@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  private ws: WebSocket;
  private callback: any;
  isOpen: boolean = false;

  constructor() {
    console.log("Constructing WebSocketService");

    this.ws = new WebSocket(WS_BASE_URL.replace("http://", "ws://"));
    this.ws.onopen = this.onSocketOpen.bind(this);
    this.ws.onclose = this.onSocketClose.bind(this);
    this.ws.onerror = this.onSocketError.bind(this);
    this.ws.onmessage = this.onSocketMessage.bind(this);
  }

  private onSocketOpen(event: Event) {
    console.log(event);
  }

  private onSocketClose(event: CloseEvent) {
    console.log(event);
  }

  private onSocketError(event: Event) {
    console.log(event);
  }

  private onSocketMessage(event: MessageEvent) {
    console.log(event);
    this.callback(event.data);
  }

  registerCallback(callback) {
    console.log("registerCallback was called");
    this.callback = callback;
  }

  send(message) {
    this.ws.send(message);
  }
}
