import { Injectable } from '@angular/core';
import {HANDLE_ERROR} from '../utility';

const WS_BASE_URL = window.location.origin;

const EVENT_WS_CLOSE_REOPEN_MS = 3000;

const MSG_PING = 'ping';
const MSG_GET_CONNECTION_TIMEOUT_SECONDS = 'get_connection_timeout_seconds';

const KEY_CONNECTION_TIMEOUT_SECONDS = 'connection_timeout_seconds';

export const NOTIF_SOCKET_OPEN = 'socket_opened';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  private ws: WebSocket;
  private callback: any;
  private messageBuffer: string[] = [];
  private connectionTimeoutSeconds = 600;  // set default to avoid race

  constructor() {
    this.initializeWebSocket();
  }

  registerCallback(callback): void {
    this.callback = callback;
  }

  send(message: string): void {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      this.messageBuffer.push(message);
    }
  }

  private initializeWebSocket() {
    this.ws = new WebSocket(
      WS_BASE_URL.replace('http://', 'ws://')
    );
    this.ws.onopen = this.onSocketOpen.bind(this);
    this.ws.onclose = this.onSocketClose.bind(this);
    this.ws.onerror = HANDLE_ERROR;
    this.ws.onmessage = this.onSocketMessage.bind(this);
  }

  private onSocketOpen(event: Event) {
    while (this.messageBuffer.length > 0) {
      this.send(this.messageBuffer.pop());
    }

    if (!this.connectionTimeoutSeconds) {
      this.send(MSG_GET_CONNECTION_TIMEOUT_SECONDS);
      return;
    }

    this.startConnectionRefreshTimer();

    // To allow users to act on re-established connections
    if (this.callback !== undefined) {
      this.callback(NOTIF_SOCKET_OPEN);
    }
  }

  private startConnectionRefreshTimer() {
    setTimeout(
      this.refreshConnection.bind(this),
      this.connectionTimeoutSeconds * 1000
    );
  }

  private refreshConnection() {
    this.send(MSG_PING);
    this.startConnectionRefreshTimer();
  }

  private onSocketClose(event: CloseEvent) {
    setTimeout(
      this.initializeWebSocket.bind(this),
      EVENT_WS_CLOSE_REOPEN_MS
    );
  }

  private onSocketMessage(event: MessageEvent) {
    const DECODED_DATA = JSON.parse(event.data);
    // console.debug(DECODED_DATA);

    if (KEY_CONNECTION_TIMEOUT_SECONDS in DECODED_DATA) {
      this.connectionTimeoutSeconds = DECODED_DATA.connection_timeout_seconds;
      this.startConnectionRefreshTimer();
      return;
    }

    this.callback(DECODED_DATA);
  }
}
