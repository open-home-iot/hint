import { Component, OnInit } from '@angular/core';

import { HumeService } from './hume.service';

@Component({
  selector: 'app-hume',
  templateUrl: './hume.component.html',
  styleUrls: ['./hume.component.scss']
})
export class HumeComponent implements OnInit {
  humes: string[];

  constructor(private humeService: HumeService) { }

  ngOnInit() {
    this.humes = this.humeService.getAllHumes();
    console.log("init hume component");
  }

  addHume(name: string) {
    this.humeService.addHume(name);
  }
}
