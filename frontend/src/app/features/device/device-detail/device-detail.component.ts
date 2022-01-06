import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {
  Device,
  DeviceService,
  DeviceState,
  StatefulAction,
} from '../device.service';
import {HomeService} from '../../home/home.service';
import {
  EventService,
  HumeEvent, NO_HUME_UUID,
  STATEFUL_ACTION
} from '../../event/event.service';


@Component({
  selector: 'app-device-detail',
  templateUrl: './device-detail.component.html',
  styleUrls: ['./device-detail.component.scss']
})
export class DeviceDetailComponent implements OnInit, OnDestroy {

  @Input() device: Device;
  // group_name -> DeviceStates
  state_groups: Map<string, DeviceState[]>;

  private subscription: number;

  constructor(private homeService: HomeService,
              private deviceService: DeviceService,
              private eventService: EventService) { }

  ngOnInit(): void {
    if (this.device.states.length > 0) {
      this.subscription = this.eventService.subscribe(
        NO_HUME_UUID,
        this.device.uuid,
        STATEFUL_ACTION,
        this.onStatefulAction.bind(this)
      );
      this.state_groups = new Map<string, DeviceState[]>();

      for (const STATE of this.device.states) {
        if (this.state_groups.has(STATE.device_state_group.group_name)) {
          this.state_groups.get(STATE.device_state_group.group_name).push(STATE);
        } else {
          this.state_groups.set(STATE.device_state_group.group_name, [STATE]);
        }
      }
    }
  }

  ngOnDestroy() {
    this.eventService.unsubscribe(this.subscription);
  }

  stateChange(newState: DeviceState) {
    this.deviceService.changeState(this.device, newState);
  }

  deleteDevice() {
    this.deviceService.delete(this.device);
  }

  private onStatefulAction(event: HumeEvent) {
    const STATEFUL_ACTION = event.content as StatefulAction;
    
    console.log(STATEFUL_ACTION);
  }
}
