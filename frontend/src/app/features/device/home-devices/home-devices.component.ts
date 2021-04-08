import { Component, OnInit, Input } from '@angular/core';

import { DeviceService, Device } from '../device.service';

@Component({
  selector: 'app-home-devices',
  templateUrl: './home-devices.component.html',
  styleUrls: ['./home-devices.component.scss']
})
export class HomeDevicesComponent implements OnInit {

  @Input() homeID: number;
  devices: Device[];

  constructor(private deviceService: DeviceService) { }

  ngOnInit(): void {
    this.deviceService.getHomeDevices(this.homeID)
      .then(this.onGetHomeDevices.bind(this))
      .catch(this.onGetHomeDevicesFailed)
  }

  onGetHomeDevices(devices: Device[]) {
    this.devices = devices;
  }

  onGetHomeDevicesFailed(error) {
    console.error(error);
  }
}
