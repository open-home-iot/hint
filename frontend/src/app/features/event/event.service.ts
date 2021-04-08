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

export const HUB_DISCOVER_DEVICES = 0;

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private subscriptionMap: {
    (subscription_id: string): {
      subscription_key: string
      callback: Function,
      event_type: number
    } 
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
    for (let subscription_id in this.subscriptionMap){
      let subMap = this.subscriptionMap[subscription_id];
 
      if(subMap.subscription_key === decoded_event.hume_uuid){
       
        if (subMap.event_type === decoded_event.event_type){
          
        let callbackObject = subMap.callback;
        callbackObject(decoded_event);
        }
      }
    }
  } 

  subscribe(subscriptionId: string, subscriptionKey: string,  eventType: number, callback: Function) {
    console.log("Subscribing to key: " + String(subscriptionKey));  

    this.subscriptionMap[subscriptionId] = {
      subscription_key : subscriptionKey,
      event_type : eventType,
      callback : callback
    }
  }

  unsubscribe(subscriptionId: string) {
    delete this.subscriptionMap[subscriptionId];
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({"home_id": homeId}));
  }
}
