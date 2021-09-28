import {Component, Input} from '@angular/core';
import {HumeEvent} from '../../event/event.service';

@Component({
  selector: 'app-device-discovered',
  templateUrl: './device-discovered.component.html',
  styleUrls: ['./device-discovered.component.scss']
})
export class DeviceDiscoveredComponent {

  @Input() discoveredDevice: HumeEvent;

  constructor() { }
}
