import {Component, ElementRef, NgZone, OnDestroy, OnInit, Renderer2, ViewChild} from "@angular/core";
import {Subscription} from "rxjs/Subscription";
import {SurveillanceService} from "../surveillance/services/surveillance.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy {

  alarmRaised: boolean;
  alarmSubscription: Subscription;

  @ViewChild('displayDateTime')
  displayDateTime: ElementRef;

  constructor(private zone: NgZone,
              private renderer: Renderer2,
              private surveillanceService: SurveillanceService) {}

  ngOnInit() {
    this.zone.runOutsideAngular(() => {
      setInterval(
        () => {
          this.renderer.setProperty(this.displayDateTime.nativeElement, 'textContent', new Date());
        }
      , 1000);
    });
    this.surveillanceService.alarmSubject.subscribe(
      next => {
        this.alarmRaised = next;
      }
    );
  }

  ngOnDestroy() {
    this.alarmSubscription.unsubscribe();
  }
}
