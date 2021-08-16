import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Device } from '../device.service';

@Component({
  selector: 'app-discovered-devices',
  templateUrl: './discovered-devices.component.html',
  styleUrls: ['./discovered-devices.component.scss']
})
export class DiscoveredDevicesComponent implements OnInit {

  @Input() devices: Device[];
  @Output() attachDevice = new EventEmitter<Device>();

  constructor() { }

  ngOnInit(): void {
  }

  attach(device: Device) {
    this.attachDevice.emit(device);
  }
}
