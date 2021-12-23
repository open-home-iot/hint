import {
  Component,
  Input, OnDestroy,
} from '@angular/core';
import {Home, HomeService} from '../../home/home.service';
import {Hume} from '../../hume/hume.service';
import {
  EventService,
  HUB_DISCOVER_DEVICES,
  HumeEvent
} from '../../event/event.service';

@Component({
  selector: 'app-device-discover',
  templateUrl: './device-discover.component.html',
  styleUrls: ['./device-discover.component.scss']
})
export class DeviceDiscoverComponent implements OnDestroy {

  @Input() home: Home;
  @Input() humes: Hume[];

  showDiscoveryBox = false;

  showDiscoveryFailure = false;
  discoveryErrorMessage = '';

  discoveredDevices: HumeEvent[] = [];

  private timeout;
  private subscriptions: number[] = [];

  constructor(private eventService: EventService,
              private homeService: HomeService) { }

  ngOnDestroy() {
    for (const SUBSCRIPTION of this.subscriptions) {
      this.eventService.unsubscribe(SUBSCRIPTION);
    }
  }

  discoverDevices() {
    clearTimeout(this.timeout);
    this.showDiscoveryBox = true;
    this.showDiscoveryFailure = false;
    this.discoveredDevices.length = 0;

    for (const SUBSCRIPTION of this.subscriptions) {
      this.eventService.unsubscribe(SUBSCRIPTION);
    }

    for (const HUME of this.humes) {
      this.subscriptions.push(
        this.eventService.subscribe(
          HUME.uuid, HUB_DISCOVER_DEVICES, this.deviceDiscovered.bind(this)
        )
      );
    }

    this.homeService.discoverDevices(this.home.id)
      .then(this.discoveryStarted.bind(this))
      .catch(this.discoveryStartFailed);

    this.timeout = setTimeout(
      this.checkDiscoveryTimeout.bind(this), 5000
    );
  }

  hideDiscoveryBox() {
    this.showDiscoveryBox = false;
  }

  private deviceDiscovered(event: HumeEvent) {
    this.discoveredDevices.push(event);
  }

  private discoveryStarted() {}
  private discoveryStartFailed(error) {
    this.showDiscoveryFailure = true;
    this.discoveryErrorMessage = 'Failed to scan the home, please try again';
    console.error(error);
  }

  private checkDiscoveryTimeout() {
    if (this.discoveredDevices.length === 0) {
      this.showDiscoveryFailure = true;
      this.discoveryErrorMessage = 'No devices found';
    }
  }
}