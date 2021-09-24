import { Component, OnInit } from '@angular/core';
import {Home} from '../../home.service';


@Component({
  selector: 'app-home-overview',
  templateUrl: './home-overview.component.html',
  styleUrls: ['./home-overview.component.scss']
})
export class HomeOverviewComponent implements OnInit {

  selectedHome: Home;

  constructor() { }

  ngOnInit() { }

  onAddHome(home: Home) {
    console.log("home overview got add home event", home);
  }
}
