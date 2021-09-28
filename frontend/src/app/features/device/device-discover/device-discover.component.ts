import {Component, Input, OnInit} from '@angular/core';
import {Home} from '../../home/home.service';

@Component({
  selector: 'app-device-discover',
  templateUrl: './device-discover.component.html',
  styleUrls: ['./device-discover.component.scss']
})
export class DeviceDiscoverComponent implements OnInit {

  @Input() home: Home;

  constructor() { }

  ngOnInit(): void {
  }

  discoverDevices() {

  }
}
