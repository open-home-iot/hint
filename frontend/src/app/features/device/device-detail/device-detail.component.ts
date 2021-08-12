import {Component, Input, OnInit} from '@angular/core';
import {
  Device,
  DeviceService,
  DeviceState,
  DeviceStateGroup
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

    for (let state of this.device.states) {
      if (this.state_groups.has(state.device_state_group.group_name)) {
        this.state_groups.get(state.device_state_group.group_name).push(state);
      } else {
        this.state_groups.set(state.device_state_group.group_name, [state]);
      }
    }
  }

  stateChange(newState: DeviceState) {
    this.deviceService.changeState(this.device, newState);
  }

  onRoomSelected(roomID: number) {
    this.deviceService.changeRoom(this.device, roomID);
  }
}
