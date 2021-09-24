import { Component, OnInit } from '@angular/core';
import {Home, HomeService} from '../../home.service';

const LS_KEY_SELECTED_HOME_ID = "selectedHomeID";

@Component({
  selector: 'app-home-overview',
  templateUrl: './home-overview.component.html',
  styleUrls: ['./home-overview.component.scss']
})
export class HomeOverviewComponent implements OnInit {

  homes: Map<number, Home>;
  selectedHome: Home;

  constructor(private homeService: HomeService) { }

  ngOnInit() {
    this.homeService.getHomes()
      .then(this.onGetHomes.bind(this))
      .catch(this.onGetHomesFailed)
  }

  onAddHome(home: Home) {
    if (this.selectedHome === undefined) {
      this.selectedHome = home;
      localStorage.setItem(LS_KEY_SELECTED_HOME_ID, String(home.id));
    }
  }

  private onGetHomes(homes: Map<number, Home>) {
    this.homes = homes;

    const SELECTED_HOME_ID = localStorage.getItem(LS_KEY_SELECTED_HOME_ID)
    if (SELECTED_HOME_ID !== null) {
      this.selectedHome = this.homes.get(Number(SELECTED_HOME_ID))
    } else {
      let iterator = this.homes.keys();
      const KEY = iterator.next();
      if (KEY.value !== undefined) {
        this.selectedHome = this.homes.get(KEY.value);
      }
    }
  }

  private onGetHomesFailed(error) {
    console.error(error);
  }
}
