import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';

import {Device, DeviceService} from '../device.service';
import { Home } from '../../home/home.service';
import {HANDLE_ERROR} from '../../../core/utility';

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.scss']
})
export class DeviceListComponent implements OnChanges {

  @Input() home: Home;
  devices: Device[];

  constructor(private deviceService: DeviceService) { }

  ngOnChanges(changes: SimpleChanges): void {
    this.deviceService.getHomeDevices(this.home.id)
      .then(this.onHomeDevicesGotten.bind(this))
      .catch(HANDLE_ERROR);
  }

  private onHomeDevicesGotten(devices: Device[]) {
    this.devices = devices;
  }
}
