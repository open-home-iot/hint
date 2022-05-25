import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {
  Device,
  DeviceService,
  DeviceState, DeviceStateGroup,
  StatefulAction,
} from '../device.service';
import {HomeService} from '../../home/home.service';
import {
  EventService,
  HumeEvent, NO_HUME_UUID,
  STATEFUL_ACTION
} from '../../event/event.service';
import {HANDLE_ERROR} from '../../../core/utility';


@Component({
  selector: 'app-device-detail',
  templateUrl: './device-detail.component.html',
  styleUrls: ['./device-detail.component.scss']
})
export class DeviceDetailComponent implements OnInit, OnDestroy {

  @Input() device: Device;
  // group_name -> DeviceStates
  stateGroups: Map<string, DeviceState[]>;
  activeState: Map<number, number> = new Map<number, number>();

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
        this.onStatefulAction.bind(this),
      );

      this.stateGroups = new Map<string, DeviceState[]>();
      for (const STATE of this.device.states) {
        if (this.stateGroups.has(STATE.group.name)) {
          this.stateGroups.get(STATE.group.name).push(STATE);
        } else {
          this.stateGroups.set(STATE.group.name, [STATE]);
        }
      }
      // Expect feedback through the event bus.
      this.deviceService.getCurrentStates(this.device);
    }
  }

  ngOnDestroy() {
    this.eventService.unsubscribe(this.subscription);
  }

  changeState(newState: DeviceState) {
    // Expect feedback through the event bus.
    this.deviceService.changeState(this.device, newState);
  }

  deleteDevice() {
    this.deviceService.delete(this.device);
  }

  private onStatefulAction(event: HumeEvent) {
    const STATEFUL_ACTION_EVENT = event.content as StatefulAction;

    this.activeState[STATEFUL_ACTION_EVENT.group_id] =
      STATEFUL_ACTION_EVENT.state_id;
  }
}
