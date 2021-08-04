import { Component, Input, OnInit } from '@angular/core';
import { Device } from '../device.service';

@Component({
  selector: 'app-discovered-device',
  templateUrl: './discovered-device.component.html',
  styleUrls: ['./discovered-device.component.scss']
})
export class DiscoveredDeviceComponent implements OnInit {

  @Input() device: Device;

  constructor() { }

  ngOnInit(): void {
  }

}
