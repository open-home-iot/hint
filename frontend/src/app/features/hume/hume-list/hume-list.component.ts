import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { HumeService, Hume } from '../hume.service';

import {EventService} from '../../event/event.service';

import { Device } from '../../device/device.service';

import { HumeEvent } from '../../event/event.service';

import {HUB_DISCOVER_DEVICES} from '../../event/event.service';

@Component({
  selector: 'app-hume-list',
  templateUrl: './hume-list.component.html',
  styleUrls: ['./hume-list.component.scss']
})
export class HumeListComponent implements OnInit, OnDestroy {

  @Input() homeId: number;
  humes: Hume[];
  deviceList: Device[] = [];

  constructor(private humeService: HumeService, private eventService: EventService) { }


  ngOnInit(): void {
    console.log("Init HUME list component");
    this.humes = this.humeService.initHomeHumes(this.homeId);
  }

  discoverDevices(humeUUID: string) {
    this.eventService.unsubscribe("123456789")
    console.log("HUME to discover devices for: " + humeUUID);
    this.humeService.discoverDevices(humeUUID).subscribe();
    this.eventService.subscribe("123456789", humeUUID, HUB_DISCOVER_DEVICES, this.onDevicesDiscovered.bind(this));

    this.deviceList = [];
  }

  onDevicesDiscovered(deviceDiscoredEvent: HumeEvent){
    for (let device of deviceDiscoredEvent.content){
      let newDevice = new Device();
      newDevice.uuid = device.uuid;
      newDevice.humeUuid = deviceDiscoredEvent.hume_uuid;
      this.deviceList.push(newDevice);
      
    }    
    console.log("the device list ");
    console.log(this.deviceList.length);
  }

  ngOnDestroy(): void {
    console.log("Shutting down HUME list component");
    this.eventService.unsubscribe("123456789")
  }
}
