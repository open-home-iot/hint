import {Component, OnDestroy, OnInit} from '@angular/core';
import {Home} from '../../home/home.service';
import {Hume} from '../../hume/hume.service';
import {GodmodeService} from '../godmode.service';
import {HANDLE_ERROR} from '../../../core/utility';
import {
  EventService, HumeEvent,
  LATENCY_TEST,
  NO_DEVICE_UUID
} from '../../event/event.service';

interface Content {
  hint_hume_sent: number;
  hint_hume_received: number;
}

@Component({
  selector: 'app-godmode-latency-testing',
  templateUrl: './godmode-latency-testing.component.html',
  styleUrls: ['./godmode-latency-testing.component.scss']
})
export class GodmodeLatencyTestingComponent implements OnInit, OnDestroy {

  selectedHome: Home;
  selectedHumes: Hume[] = [];

  testing: boolean = false;
  hintHumeLatency: number = 0;

  private subscriptions: number[] = [];

  constructor(private godmodeService: GodmodeService,
              private eventService: EventService) { }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.unsubscribe();
  }

  homeSelected(home: Home) {
    this.selectedHome = home;
    this.godmodeService.getHumes(home)
      .then((humes: Hume[]) => this.updateHumes(humes))
      .catch(error => HANDLE_ERROR(error));
  }

  toggleLatencyTest() {
    /*
    If testing isn't already started, start it.
      - Subscribe to hume events.
      - Send request to latency test endpoint.
      - On answer, check if testing still started, and if true send another request.

    If testing is started, stop it.
      - Unsubscribe from hume events.
     */

    if (this.selectedHumes.length > 0 && !this.testing) {
      this.testing = true;
      this.subscribe();
      this.latencyTest();
    } else {
      this.testing = false;
      this.unsubscribe();
    }
  }

  private updateHumes(humes: Hume[]): void {
    this.selectedHumes.length = 0;
    for (let hume of humes) {
      this.selectedHumes.push(hume);
      this.eventService.monitorHume(hume.uuid);
    }
  }

  private subscribe(): void {
    for (let hume of this.selectedHumes) {
        this.subscriptions.push(this.eventService.subscribe(
          hume.uuid, NO_DEVICE_UUID, LATENCY_TEST, this.onHumeEvent.bind(this)
        ));
      }
  }

  private unsubscribe(): void {
    while (this.subscriptions.length != 0) {
      this.eventService.unsubscribe(this.subscriptions.pop());
    }
  }

  private latencyTest(): void {
    this.godmodeService.latencyTest(this.selectedHumes)
      .then(() => null)
      .catch(error => HANDLE_ERROR(error));
  }

  private onHumeEvent(event: HumeEvent): void {
    /*
    The event contains sent/received timings in the content-field.
     */
    let content: Content = event.content;
    this.hintHumeLatency = content.hint_hume_received / 1000000 -
      content.hint_hume_sent / 1000000;

    setTimeout(() => {
      // Still testing, send another test signal after a small delay.
      if (this.testing) {
        this.godmodeService.latencyTest(this.selectedHumes)
          .then(() => null)
          .catch(error => HANDLE_ERROR(error));
      }
    }, 500);
  }
}
