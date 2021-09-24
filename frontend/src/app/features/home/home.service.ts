import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Home {
  id: number;
  name: string;
}

export interface Room {
  id: number;
  home: number;
  name: string;
}

const HOMES_URL = window.location.origin + '/api/homes';

@Injectable()
export class HomeService {

  constructor(private httpClient: HttpClient) { }

  createHome(name: string): Promise<Home> {
    return new Promise<Home>((resolve, reject) => {
      this.httpClient.post(HOMES_URL, {name})
        .subscribe(
          (home: Home) => {
            resolve(home);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  getHomeRooms(bla): any {}

  getHomes(): any {}

  getRoom(bla): any {}
}
