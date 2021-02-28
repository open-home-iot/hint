import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpService } from '../../core/http/http.service';
import { EventService } from '../event/event.service';

const HOMES_URL = window.location.origin + "/api/homes/"

export class Home {
  id: number;
  name: string;
}

export class Room {
  id: number;
  name: string;
}

@Injectable()
export class HomeService {

  homes: Home[] = [];

  constructor(private httpClient: HttpClient,
              private eventService: EventService) {
    console.log("Constructing HomeService");
    this.httpClient.get(HOMES_URL)
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
    this.httpClient.post(HOMES_URL, {name: name})
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

  private getHomeRoomsUrl(homeID: number) {
    return HOMES_URL + String(homeID) + "/rooms";
  }

  getHomeRooms(homeID: number) {
    return this.httpClient.get<Room[]>(this.getHomeRoomsUrl(homeID))
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error("An error occured:", error.error.message);
    } else {
      console.error(
        `Backend returned code: ${error.status}, ` +
        `body was: ${error.error}`
      );
    }

    return throwError("Oops, that didn't go so well...");
  }
}
