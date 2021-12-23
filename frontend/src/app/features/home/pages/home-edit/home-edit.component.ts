import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Home, HomeService} from '../../home.service';

@Component({
  selector: 'app-home-edit',
  templateUrl: './home-edit.component.html',
  styleUrls: ['./home-edit.component.scss']
})
export class HomeEditComponent implements OnInit {

  home: Home;
  // To avoid string interpolation error on page load.
  homeName: string = "";

  constructor(private route: ActivatedRoute,
              private homeService: HomeService) { }

  ngOnInit(): void {
    this.homeService.getHome(Number(this.route.snapshot.params['id']))
      .then(this.onGetHome.bind(this))
      .catch(this.onGetHomeFailed);
  }

  private onGetHome(home: Home) {
    this.home = home;
    this.homeName = home.name;
  }

  private onGetHomeFailed(error) {
    console.error(error);
  }
}
