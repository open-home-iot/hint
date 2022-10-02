import { Component, OnInit } from '@angular/core';
import {Home} from '../../../home/home.service';
import {Hume} from '../../../hume/hume.service';

@Component({
  selector: 'app-godmode-overview',
  templateUrl: './godmode-overview.component.html',
  styleUrls: ['./godmode-overview.component.scss']
})
export class GodmodeOverviewComponent implements OnInit {

  home: Home;
  hume: Hume;

  constructor() { }

  ngOnInit(): void {
  }

  homeSelected(home: Home) {
    this.home = home;
  }

  humeSelected(hume: Hume) {
    this.hume = hume;
  }
}
