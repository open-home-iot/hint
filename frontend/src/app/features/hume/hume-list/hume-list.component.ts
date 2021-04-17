import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { Utility } from '../../../core/utility';
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
  deviceList: Device[] = [];

  private subscriptionID: string

  constructor(private humeService: HumeService, private eventService: EventService) { }

  ngOnInit(): void {
    this.humeService.getHomeHumes(this.homeID)
      .then(this.onGetHumes.bind(this))
      .catch(this.onGetHumesFailed);
    this.subscriptionID = Utility.generateRandomID();
  }

  ngOnDestroy(): void {
    this.eventService.unsubscribe(this.subscriptionID);
  }

  discoverDevices(humeUUID: string) {
    this.deviceList = [];
    this.eventService.unsubscribe(this.subscriptionID);

    this.subscriptionID = Utility.generateRandomID()
    this.eventService.subscribe(
      this.subscriptionID, humeUUID, HUB_DISCOVER_DEVICES, this.onDevicesDiscovered.bind(this)
    );

    this.humeService.discoverDevices(humeUUID).subscribe();
  }

  private onGetHumes(humes: Hume[]): void {
    this.humes = humes;
  }

  private onGetHumesFailed(error) {
    console.log('Get humes failed: ', error)
  }

  private onDevicesDiscovered(deviceDiscoveredEvent: HumeEvent) {
    this.deviceList = deviceDiscoveredEvent.content;
  }
}
