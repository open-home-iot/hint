import { Component, OnInit, Input } from '@angular/core';

import { HumeService, Hume } from '../hume.service';

import { Device } from '../../device/device.service';

@Component({
  selector: 'app-hume-list',
  templateUrl: './hume-list.component.html',
  styleUrls: ['./hume-list.component.scss']
})
export class HumeListComponent implements OnInit {

  @Input() homeId: number;
  humes: Hume[];

  constructor(private humeService: HumeService) { }

  ngOnInit(): void {
    console.log("Init HUME list component");
    this.humes = this.humeService.initHomeHumes(this.homeId);
  }

  discoverDevices(humeUUID: string) {
    console.log("HUME to discover devices for: " + humeUUID);
    this.humeService.discoverDevices(humeUUID).subscribe();
  }
}
