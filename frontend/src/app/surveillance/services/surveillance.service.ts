import { Injectable } from "@angular/core";

import { BehaviorSubject } from "rxjs/BehaviorSubject";

import { Event, EventHandlerService } from "../../events/services/event-handler.service";
import {RequestService} from "../../api-interface/request.service";


const CONFIG_URL = 'http://' + window.location.hostname + ':8000/api/surveillance/pictures/';


@Injectable()
export class SurveillanceService {
  alarmSubject: BehaviorSubject<boolean>;

  alarmState: boolean;
  pictureMode: boolean;

  constructor(private requestService: RequestService,
              private eventListener: EventHandlerService) {
    this.alarmSubject = new BehaviorSubject<boolean>(false);
    eventListener.events.subscribe(
      (next: Event) => {
          switch (next.type) {
            case 'event.alarm':
              this.alarmSubject.next(next.content == 'on');
              break;
            default:
              break;
          }
      }
    );
    this.alarmState = false;
    this.pictureMode = false;
  }

  initSurveillanceConfig() {
    this.requestService.get();
  }
}
