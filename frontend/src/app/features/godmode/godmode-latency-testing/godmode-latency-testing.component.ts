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
  hint_hume_returned: number;
}

interface HumeStats {
  oneWay: number;
  roundTrip: number;
}

@Component({
  selector: 'app-godmode-latency-testing',
  templateUrl: './godmode-latency-testing.component.html',
  styleUrls: ['./godmode-latency-testing.component.scss']
})
export class GodmodeLatencyTestingComponent implements OnInit, OnDestroy {

  selectedHome: Home;
  selectedHumes: Hume[] = [];

  testing = false;
  humeStats: Map<string, HumeStats> = new Map<string, HumeStats>();

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
    if (this.selectedHumes.length < 1) {
      HANDLE_ERROR('can\'t latency test something that doesn\'t exist, ' +
        'you dingus.');
      return;
    }

    if (!this.testing) {
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
    for (const HUME of humes) {
      this.selectedHumes.push(HUME);
      this.humeStats.set(HUME.uuid, { oneWay: 0, roundTrip: 0 });
      this.eventService.monitorHume(HUME.uuid);
    }
  }

  private subscribe(): void {
    for (const HUME of this.selectedHumes) {
        this.subscriptions.push(this.eventService.subscribe(
          HUME.uuid, NO_DEVICE_UUID, LATENCY_TEST, this.onHumeEvent.bind(this)
        ));
      }
  }

  private unsubscribe(): void {
    while (this.subscriptions.length !== 0) {
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
    const CONTENT: Content = event.content;
    const STATS = this.humeStats.get(event.uuid);
    STATS.oneWay = CONTENT.hint_hume_received / 1000000 -
      CONTENT.hint_hume_sent / 1000000;
    STATS.roundTrip = CONTENT.hint_hume_returned / 1000000 -
      CONTENT.hint_hume_sent / 1000000;

    window.setTimeout(() => {
      // Still testing, send another test signal after a small delay.
      if (this.testing) {
        this.godmodeService.latencyTest(this.selectedHumes)
          .then(() => null)
          .catch(error => HANDLE_ERROR(error));
      }
    }, 500);
  }
}
