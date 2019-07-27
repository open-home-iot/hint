import { Component, OnInit } from '@angular/core';

import { HomeService } from './home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  homes: string[];

  constructor(private homeService: HomeService) { }

  ngOnInit() {
    this.homes = this.homeService.getAllHomes();
    console.log("init home component");
  }

  addHome(name: string) {
    this.homeService.addHome(name);
  }
}
