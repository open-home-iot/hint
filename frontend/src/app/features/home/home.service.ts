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

  private homes: Map<number, Home>;

  constructor(private httpClient: HttpClient) { }

  createHome(name: string): Promise<Home> {
    return new Promise<Home>((resolve, reject) => {
      this.httpClient.post(HOMES_URL, {name})
        .subscribe(
          (home: Home) => {
            this.homes.set(home.id, home);
            resolve(home);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  getHomes(): Promise<Map<number, Home>> {
    if (this.homes !== undefined) {
      return Promise.resolve(this.homes);
    }

    return new Promise<Map<number, Home>>((resolve, reject) => {
      this.httpClient.get(HOMES_URL)
        .subscribe(
          (homes: Home[]) => {
            this.refreshHomes(homes);
            resolve(this.homes);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  discoverDevices(homeID: number): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.httpClient.get(this.discoverDevicesUrl(homeID))
        .subscribe(
          _ok => {
            resolve();
          },
          error => {
            reject(error);
          }
        );
    });

  }

  getHomeRooms(bla): any {}

  getRoom(bla): any {}

  private refreshHomes(homes: Home[]) {
    if (this.homes === undefined) {
      this.homes = new Map<number, Home>();
    }

    this.homes.clear();
    for (const HOME of homes) {
      this.homes.set(HOME.id, HOME);
    }
  }

  private discoverDevicesUrl(homeID: number) {
    return HOMES_URL + "/" + String(homeID) + "/devices/discover";
  }
}
