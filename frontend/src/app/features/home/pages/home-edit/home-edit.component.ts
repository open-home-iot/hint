import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Home, HomeService} from '../../home.service';
import {Hume, HumeService} from '../../../hume/hume.service';

@Component({
  selector: 'app-home-edit',
  templateUrl: './home-edit.component.html',
  styleUrls: ['./home-edit.component.scss']
})
export class HomeEditComponent implements OnInit {

  home: Home;
  // To avoid string interpolation error on page load.
  homeName: string = "";
  humes: Hume[];

  constructor(private route: ActivatedRoute,
              private homeService: HomeService,
              private humeService: HumeService) { }

  ngOnInit(): void {
    this.homeService.getHome(Number(this.route.snapshot.params['id']))
      .then(this.onGetHome.bind(this))
      .catch(this.onGetHomeFailed);

    this.humeService.getHomeHumes(Number(this.route.snapshot.params['id']))
      .then(this.onGetHomeHumes.bind(this))
      .catch(this.onGetHomeHumesFailed);
  }

  private onGetHome(home: Home) {
    this.home = home;
    this.homeName = home.name;
  }

  private onGetHomeFailed(error) {
    console.error(error);
  }

  private onGetHomeHumes(humes: Hume[]) {
    this.humes = humes;
  }

  private onGetHomeHumesFailed(error) {
    console.error(error);
  }
}
