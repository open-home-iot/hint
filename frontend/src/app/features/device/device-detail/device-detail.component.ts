import {Component, Input, OnInit} from '@angular/core';
import {Device, DeviceService} from '../device.service';
import {HomeService} from '../../home/home.service';


@Component({
  selector: 'app-device-detail',
  templateUrl: './device-detail.component.html',
  styleUrls: ['./device-detail.component.scss']
})
export class DeviceDetailComponent implements OnInit {

  @Input() device: Device;

  constructor(private homeService: HomeService,
              private deviceService: DeviceService) { }

  ngOnInit(): void { }

  onRoomSelected(roomID: number) {
    this.deviceService.changeRoom(this.device, roomID);
  }
}
