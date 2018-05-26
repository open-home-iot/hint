import { Component, OnInit } from '@angular/core';

import { RequestService } from '../api-interface/request.service';
import { SurveillanceService } from "./services/surveillance.service";
import { Subscription } from "rxjs/Subscription";


@Component({
  selector: 'app-surveillance',
  templateUrl: './surveillance.component.html',
  styleUrls: ['./surveillance.component.css']
})
export class SurveillanceComponent implements OnInit {
  alarmRaised: boolean;
  alarmSubscription: Subscription;

  currentDisplayDate: Date;

  pictures: string[];
  alarmHistory: string[]; // format: {date: date}


  constructor(private requestService: RequestService,
              private surveillanceService: SurveillanceService) {}

  ngOnInit() {
    console.log("Initiated surveillance component");
    this.alarmSubscription = this.surveillanceService.alarmSubject.subscribe(
      next => {
        this.alarmRaised = next;
      }
    );
    this.initServiceData();
  }

  initServiceData() {
    // Get initial date
    this.currentDisplayDate = this.surveillanceService.date;

    // bindings
    this.pictures = this.surveillanceService.pictures;
    this.alarmHistory = this.surveillanceService.alarmHistory;
  }

  stepDate(forward: boolean) {
    const monthChange = forward ? 1 : -1;

    let newDate = new Date(this.currentDisplayDate);
    newDate.setMonth(newDate.getMonth() + (monthChange));
    this.currentDisplayDate = newDate;

    this.surveillanceService.stepDate(newDate);
  }

  stepPictures(forward: boolean) {
    this.surveillanceService.stepPictures(forward)
  }

  stepHistory(forward: boolean) {
    this.surveillanceService.stepHistory(forward);
  }
}
