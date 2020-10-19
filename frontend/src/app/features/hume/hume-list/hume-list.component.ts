import { Component, OnInit, Input } from '@angular/core';

import { HumeService, Hume } from '../hume.service';

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

  pairHume(humeId: number) {
    console.log("Pairing HUME: " + String(humeId));
    this.humeService.pairHume(this.homeId, humeId);
  }
}
