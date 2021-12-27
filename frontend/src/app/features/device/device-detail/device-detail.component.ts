import {Component, Input, OnInit} from '@angular/core';
import {
  Device,
  DeviceService,
  DeviceState,
} from '../device.service';
import {HomeService} from '../../home/home.service';


@Component({
  selector: 'app-device-detail',
  templateUrl: './device-detail.component.html',
  styleUrls: ['./device-detail.component.scss']
})
export class DeviceDetailComponent implements OnInit {

  @Input() device: Device;
  // group_name -> DeviceStates
  state_groups: Map<string, DeviceState[]>;

  constructor(private homeService: HomeService,
              private deviceService: DeviceService) { }

  ngOnInit(): void {
    this.state_groups = new Map<string, DeviceState[]>();

    for (const STATE of this.device.states) {
      if (this.state_groups.has(STATE.device_state_group.group_name)) {
        this.state_groups.get(STATE.device_state_group.group_name).push(STATE);
      } else {
        this.state_groups.set(STATE.device_state_group.group_name, [STATE]);
      }
    }
  }

  stateChange(newState: DeviceState) {
    this.deviceService.changeState(this.device, newState);
  }

  deleteDevice() {
    this.deviceService.delete(this.device);
  }
}
