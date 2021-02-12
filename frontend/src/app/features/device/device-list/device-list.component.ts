import { Component, Input, OnInit } from '@angular/core';
import {Device} from '../device.service'

@Component({
  selector: 'app-device-list',
  templateUrl: './device-list.component.html',
  styleUrls: ['./device-list.component.scss']
})
export class DeviceListComponent implements OnInit {

  @Input() deviceList: Device[]; 

  constructor() { }

  ngOnInit() {
  }

}
