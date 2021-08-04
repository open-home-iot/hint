import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { HumeService, Hume } from '../hume.service';
import { EventService, HumeEvent, HUB_DISCOVER_DEVICES } from '../../event/event.service';

import { Device } from '../../device/device.service';

@Component({
  selector: 'app-hume-list',
  templateUrl: './hume-list.component.html',
  styleUrls: ['./hume-list.component.scss']
})
export class HumeListComponent implements OnInit, OnDestroy {

  @Input() homeID: number;
  humes: Hume[];
  discoveredDevices: Device[] = [];

  private subscriptionID: string;

  constructor(private humeService: HumeService,
              private eventService: EventService) { }

  ngOnInit(): void {
    this.humeService.getHomeHumes(this.homeID)
      .then(this.onGetHumes.bind(this))
      .catch(this.onGetHumesFailed);
  }

  ngOnDestroy(): void {
    this.eventService.unsubscribe(this.subscriptionID);
  }

  discoverDevices(humeUUID: string) {
    this.discoveredDevices = [];

    if (this.subscriptionID) {
      this.eventService.unsubscribe(this.subscriptionID);
    }

    this.subscriptionID = this.eventService.subscribe(
      humeUUID,
      HUB_DISCOVER_DEVICES,
      this.onDevicesDiscovered.bind(this)
    );

    this.humeService.discoverDevices(humeUUID).subscribe();
  }

  private onGetHumes(humes: Hume[]): void {
    this.humes = humes;
  }

  private onGetHumesFailed(error) {
    console.error(error);
  }

  private onDevicesDiscovered(deviceDiscoveredEvent: HumeEvent) {
    this.discoveredDevices = deviceDiscoveredEvent.content;
  }
}
