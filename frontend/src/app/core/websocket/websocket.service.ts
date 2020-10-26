import { Injectable } from '@angular/core';


const WS_BASE_URL = window.location.origin + "/ws/";


@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  private ws: WebSocket;
  private callback: any;

  constructor() {
    console.log("Constructing WebSocketService");

    this.ws = new WebSocket(WS_BASE_URL.replace("http://", "ws://") + "test/1");
    this.ws.onopen = this.onSocketOpen.bind(this);
    this.ws.onclose = this.onSocketClose.bind(this);
    this.ws.onerror = this.onSocketError.bind(this);
    this.ws.onmessage = this.onSocketMessage.bind(this);
  }

  private onSocketOpen(event: any) {
    console.log("Socket opened!");
  }

  private onSocketClose(event: any) {
    console.log("Socket closed!");
  }

  private onSocketError(event: any) {
    console.log("Socket error!");
  }

  private onSocketMessage(event: any) {
    console.log("Socket message received:");
    console.log(event);
    this.callback(event);
  }

  subscribe(callback) {
    console.log("Subscribe was called");
    this.callback = callback;
  }

  send(message) {
    this.ws.send(message);
  }
}
