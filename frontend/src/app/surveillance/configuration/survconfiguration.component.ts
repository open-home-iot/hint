import {Component, OnDestroy, OnInit} from '@angular/core';
import {SurveillanceService} from "../services/surveillance.service";
import {Subscription} from "rxjs/Subscription";


export interface SurveillanceConfiguration {
  alarmState: boolean,
  pictureMode: boolean
}
@Component({
  selector: 'app-surveillance-configuration',
  templateUrl: './survconfiguration.component.html',
  styleUrls: ['./survconfiguration.component.css']
})
export class SurvconfigurationComponent implements OnInit, OnDestroy {
  configurationSubscription: Subscription;
  configuration: SurveillanceConfiguration;

  constructor(private surveillanceService: SurveillanceService) {}

  ngOnInit() {
    this.configurationSubscription = this.surveillanceService.configurationSubject.subscribe(
      next => {
        this.configuration = next;
      }
    );
  }

  ngOnDestroy() {
    this.configurationSubscription.unsubscribe();
  }

  onChange() {
    this.surveillanceService.configurationChanged(this.configuration);
  }


}
