import { Component, OnInit } from '@angular/core';
import {Home, HomeService} from '../../home.service';
import {Hume} from '../../../hume/hume.service';

const LS_KEY_SELECTED_HOME_ID = 'selectedHomeID';

@Component({
  selector: 'app-home-overview',
  templateUrl: './home-overview.component.html',
  styleUrls: ['./home-overview.component.scss']
})
export class HomeOverviewComponent implements OnInit {

  homes: Map<number, Home>;
  humes: Hume[];
  selectedHome: Home;

  constructor(private homeService: HomeService) { }

  ngOnInit() {
    this.homeService.getHomes()
      .then(this.onGetHomes.bind(this))
      .catch(this.onGetHomesFailed);
  }

  homeAdded(home: Home) {
    if (this.selectedHome === undefined) {
      this.selectedHome = home;
      localStorage.setItem(LS_KEY_SELECTED_HOME_ID, String(home.id));
    }
  }

  homeSelected(home: Home) {
    this.selectedHome = home;
    localStorage.setItem(LS_KEY_SELECTED_HOME_ID, String(home.id));
  }

  homeHumes(humes: Hume[]) {
    this.humes = humes;
  }

  private onGetHomes(homes: Map<number, Home>) {
    this.homes = homes;

    const SELECTED_HOME_ID = localStorage.getItem(LS_KEY_SELECTED_HOME_ID);
    if (SELECTED_HOME_ID !== null) {
      this.selectedHome = this.homes.get(Number(SELECTED_HOME_ID));
    }

    // A previous selected home may have been deleted or a home favourite may
    // not yet have been selected.
    if (this.selectedHome === undefined) {
      localStorage.removeItem(LS_KEY_SELECTED_HOME_ID);
      const ITERATOR = this.homes.keys();
      const KEY = ITERATOR.next();
      if (KEY.value !== undefined) {
        this.selectedHome = this.homes.get(KEY.value);
        localStorage.setItem(LS_KEY_SELECTED_HOME_ID, KEY.value);
      }
    }
  }

  private onGetHomesFailed(error) {
    console.error(error);
  }
}
