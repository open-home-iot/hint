import { Component, OnInit } from '@angular/core';

import { HomeService, Home } from '../home.service';


@Component({
  selector: 'app-home-list',
  templateUrl: './home-list.component.html',
  styleUrls: ['./home-list.component.scss']
})
export class HomeListComponent implements OnInit {

  homes: Home[];

  constructor(private homeService: HomeService) { }

  ngOnInit() {
    this.homes = this.homeService.getHomes();
  }
}
