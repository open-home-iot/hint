import { Injectable } from '@angular/core';

import { WebSocketService } from '../../core/websocket/websocket.service';
import { Hume } from '../hume/hume.service';

export class HumeEvent {
  home_id: number;
  hume_uuid: string;
  device_uuid: string;
  event_type: string;
  content: any;
}

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap: {
    (subscriptionKey: string): {
      subscription_id: string
      callback: Function,
      event_type: string
    }[] 
  } | {} = {};

  /*
{ "hubIDX2": [function1, function2, function3] }

  { "hubIDX2": [
    {"consumer": hume_list, "eventType": "discover_devices", "callback": function1},
    {"eventType": "discover_devices" ,"callback": function2}
    ] 
  }
  */

  constructor(private webSocketService: WebSocketService) {
    this.webSocketService.registerCallback(this.onEvent.bind(this));
  }

  onEvent(event: string) {
    let decoded_event: HumeEvent = JSON.parse(event);
    console.log(decoded_event);
    
    if (decoded_event.hume_uuid in this.subscriptionMap) {
      for (let callbackObject of this.subscriptionMap[decoded_event.hume_uuid]) {
         if (decoded_event.event_type == callbackObject.event_type){
            callbackObject(decoded_event);
         }
      }
    }
  }

  subscribe(subscriptionKey: string, subscriptionId: string, eventType: string, callback: Function) {
    console.log("Subscribing to key: " + String(subscriptionKey));
    if (!(subscriptionKey in this.subscriptionMap)) {
      this.subscriptionMap[subscriptionKey] = [];
    }
    this.subscriptionMap[subscriptionKey].push(callback);
    console.log("this is the subscriptionmap")
    console.log(this.subscriptionMap)
    console.log("end of subscriptionmap")
  }

  unsubscribe(subscriptionKey: string, subscriptionId: string, eventType: string, callback: Function) {
    console.log(this.subscriptionMap);

    delete this.subscriptionMap[subscriptionKey];
    console.log(this.subscriptionMap);
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({"home_id": homeId}));
  }
}
