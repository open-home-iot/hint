import { Component, OnInit } from '@angular/core';

import { DeviceService } from './device.service';

@Component({
  selector: 'app-device',
  templateUrl: './device.component.html',
  styleUrls: ['./device.component.scss']
})
export class DeviceComponent implements OnInit {
  devices: string[];

  constructor(private deviceService: DeviceService) { }

  ngOnInit() {
    this.devices = this.deviceService.getAllDevices();
    console.log("init device component");
  }

  addDevice(name: string) {
    this.deviceService.addDevice(name);
  }
}
