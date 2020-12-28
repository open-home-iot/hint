import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';
import { EventService } from '../event/event.service';


const HOME_URL = window.location.origin + "/api/homes/"


export class Home {
  id: number;
  name: string;
}

@Injectable()
export class HomeService {

  homes: Home[] = [];

  constructor(private httpService: HttpService,
              private eventService: EventService) {
    console.log("Constructing HomeService");
    this.httpService.get(HOME_URL)
      .subscribe(
        (homes: Home[]) => {
          console.log("Successfully got all HOMES!");
          for (let home of homes) {
            this.addHome(home);
          }
        },
        error => {
          console.log(error);
        }
      );
  }

  addHome(home: Home) {
    this.homes.push(home);

    // This ensures that we get dynamic updates for the new homeId
    this.eventService.monitorHome(home.id);
  }

  createHome(name: string) {
    console.log("HomeService: Creating HOME");
    this.httpService.post(HOME_URL, {name: name})
      .subscribe(
        (home: Home) => {
          console.log("Successfully created HOME instance!");
          this.addHome(home);
        },
        error => {
          console.log(error);
        }
      );
  }

}
