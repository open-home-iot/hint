import { Component, Input, OnInit } from '@angular/core';
import { Device } from '../device.service';

@Component({
  selector: 'app-discovered-devices',
  templateUrl: './discovered-devices.component.html',
  styleUrls: ['./discovered-devices.component.scss']
})
export class DiscoveredDevicesComponent implements OnInit {

  @Input() devices: Device[];

  constructor() { }

  ngOnInit(): void {}
}
