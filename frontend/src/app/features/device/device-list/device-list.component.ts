import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';

import {Device, DeviceService} from '../device.service';
import { Home } from '../../home/home.service';

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.scss']
})
export class DeviceListComponent implements OnChanges {

  @Input() home: Home;
  devices: Device[]

  constructor(private deviceService: DeviceService) { }

  ngOnChanges(changes: SimpleChanges): void {
    this.deviceService.getHomeDevices(this.home.id)
      .then(this.onHomeDevicesGotten.bind(this))
      .catch(this.onHomeDevicesGetFailed)
  }

  private onHomeDevicesGotten(devices: Device[]) {
    this.devices = devices;
  }

  private onHomeDevicesGetFailed(error) {
    console.error(error);
  }
}
