import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-room-devices',
  templateUrl: './room-devices.component.html',
  styleUrls: ['./room-devices.component.scss']
})
export class RoomDevicesComponent implements OnInit {

  @Input() roomID: number;

  constructor() { }

  ngOnInit(): void {
  }

}
