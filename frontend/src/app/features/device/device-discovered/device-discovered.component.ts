import {Component, Input} from '@angular/core';
import {DiscoveredDevice} from '../device.service';

@Component({
  selector: 'app-device-discovered',
  templateUrl: './device-discovered.component.html',
  styleUrls: ['./device-discovered.component.scss']
})
export class DeviceDiscoveredComponent {

  @Input() discoveredDevice: DiscoveredDevice;

  constructor() { }
}
