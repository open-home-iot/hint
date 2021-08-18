import {Component, Input, OnInit} from '@angular/core';
import {Device, DeviceService} from '../device.service';

@Component({
  selector: 'app-room-devices',
  templateUrl: './room-devices.component.html',
  styleUrls: ['./room-devices.component.scss']
})
export class RoomDevicesComponent implements OnInit {

  @Input() roomID: number;
  @Input() homeID: number;
  devices: Device[];

  constructor(private deviceService: DeviceService) { }

  ngOnInit(): void {
    this.deviceService.getRoomDevices(this.homeID, this.roomID)
      .then(this.onGetRoomDevices.bind(this))
      .catch(this.onGetRoomDevicesFailed);
  }

  onGetRoomDevices(devices: Device[]) {
    this.devices = devices;
  }

  onGetRoomDevicesFailed(error) {
    console.error(error);
  }
}
