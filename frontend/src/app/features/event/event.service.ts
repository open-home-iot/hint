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
    (subscription_id: string): {
      subscription_key: string
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

    for (let sub_id in this.subscriptionMap){
      let subMap = this.subscriptionMap[sub_id];
      if(subMap.subscription_key.equals(decoded_event.hume_uuid)){
        if (subMap.event_type.equals(decoded_event.event_type)){
        let megaObject = subMap.callback;
        megaObject(decoded_event);
      }
    }
  }
    

/*
   for (let callbackObject of subMap.hume_uuid) {
          if (subMap.event_type == callbackObject.event_type){
             callbackObject(decoded_event);
          }
       }
*/

    if (decoded_event.hume_uuid in this.subscriptionMap) {
      for (let callbackObject of this.subscriptionMap[decoded_event.hume_uuid]) {
         if (decoded_event.event_type == callbackObject.event_type){
            callbackObject(decoded_event);
         }
      }
    }
  }

  subscribe(subscriptionId: string, subscriptionKey: string,  eventType: string, callback: Function) {
    console.log("Subscribing to key: " + String(subscriptionKey));
    if (!(subscriptionId in this.subscriptionMap)) {
      this.subscriptionMap[subscriptionId] = [];
    }
    this.subscriptionMap[subscriptionId].push(callback, subscriptionKey, eventType);
    console.log("this is the subscriptionmap")
    console.log(this.subscriptionMap)
    console.log("end of subscriptionmap")
  }

  unsubscribe(subscriptionId: string) {
    console.log(this.subscriptionMap);

    delete this.subscriptionMap[subscriptionId];
    console.log(this.subscriptionMap);
  }

  monitorHome(homeId: number) {
    // This will cause events related to this home to arrive as WS messages
    // in the onEvent method.
    this.webSocketService.send(JSON.stringify({"home_id": homeId}));
  }
}
