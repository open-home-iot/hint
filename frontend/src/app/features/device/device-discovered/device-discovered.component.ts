import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {AttachedDevice, DiscoveredDevice} from '../device.service';
import {HumeService} from '../../hume/hume.service';
import {HANDLE_ERROR} from '../../../core/utility';
import {
  DEVICE_ATTACHED,
  EventService,
  HumeEvent
} from '../../event/event.service';

@Component({
  selector: 'app-device-discovered',
  templateUrl: './device-discovered.component.html',
  styleUrls: ['./device-discovered.component.scss']
})
export class DeviceDiscoveredComponent implements OnInit, OnDestroy {

  @Input() discoveredDevice: DiscoveredDevice;

  attached: boolean;
  private subscription: number;

  constructor(private humeService: HumeService,
              private eventService: EventService) { }

  ngOnInit() {
    this.subscription = this.eventService.subscribe(
      this.discoveredDevice.hume,
      DEVICE_ATTACHED,
      this.onDeviceAttached.bind(this)
    );
  }

  ngOnDestroy() {
    this.eventService.unsubscribe(this.subscription);
  }

  connect() {
    this.humeService.attach(this.discoveredDevice)
      .then(null)
      .catch(HANDLE_ERROR);
  }

  private onDeviceAttached(event: HumeEvent) {
    const ATTACH_EVENT = event.content as AttachedDevice;

    if (ATTACH_EVENT.success &&
      (ATTACH_EVENT.identifier === this.discoveredDevice.identifier)) {
      this.attached = true;
    }
  }
}
