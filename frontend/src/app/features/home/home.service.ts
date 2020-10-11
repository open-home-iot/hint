import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';


const HOME_URL = window.location.origin + "/api/home/"


export class Home {
  id: number;
  name: string;
}

@Injectable()
export class HomeService {

  homes: Home[] = [];

  constructor(private httpService: HttpService) {
    console.log("Constructing HomeService");
    this.httpService.get(HOME_URL)
      .subscribe(
        (homes: Home[]) => {
          console.log("Successfully got all HOMES!");
          for (let home of homes) {
            this.homes.push(home);
          }
        },
        error => {
          console.log("Failed to get HOMES!");
          console.log(error);
        }
      );
  }

  addHome(name: string) {
    console.log("HomeService: Creating HOME");
    this.httpService.post(HOME_URL, {name: name})
      .subscribe(
        (home: Home) => {
          console.log("Successfully created HOME instance!");
          this.homes.push(home);
        },
        error => {
          console.log(error);
        }
      );
  }

}
