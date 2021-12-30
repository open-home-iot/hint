import {Component, Input} from '@angular/core';
import {DiscoveredDevice} from '../device.service';
import {HumeService} from '../../hume/hume.service';
import {HANDLE_ERROR} from '../../../core/utility';

@Component({
  selector: 'app-device-discovered',
  templateUrl: './device-discovered.component.html',
  styleUrls: ['./device-discovered.component.scss']
})
export class DeviceDiscoveredComponent {

  @Input() discoveredDevice: DiscoveredDevice;

  attached: boolean;

  constructor(private humeService: HumeService) { }

  connect() {
    this.humeService.attach(this.discoveredDevice)
      .then(this.onAttach.bind(this))
      .catch(HANDLE_ERROR);
  }

  private onAttach() {
    this.attached = true;
  }
}
