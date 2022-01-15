import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Home {
  id: number;
  name: string;
}

const HOMES_URL = window.location.origin + '/api/homes';

@Injectable()
export class HomeService {

  private homes: Map<number, Home>;

  constructor(private httpClient: HttpClient) { }

  private static discoverDevicesUrl(homeID: number) {
    return HOMES_URL + '/' + String(homeID) + '/devices/discover';
  }

  private static homeUrl(homeID: number): string {
    return HOMES_URL + '/' + String(homeID);
  }

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
            this.setHomes(homes);
            resolve(this.homes);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  getHome(homeID: number): Promise<Home> {
    if (this.homes !== undefined) {
      return Promise.resolve(this.homes.get(homeID));
    }

    return new Promise<Home>((resolve, reject) => {
      this.httpClient.get(HOMES_URL)
        .subscribe(
          (homes: Home[]) => {
            this.setHomes(homes);
            resolve(this.homes.get(homeID));
          },
          error => {
            reject(error);
          }
        );
    });
  }

  changeHome(home: Home, newName: string): Promise<Home> {
    return new Promise<Home>((resolve, reject) => {
      this.httpClient.patch(HomeService.homeUrl(home.id),
        {
          name: newName,
        })
        .subscribe(
          (patchedHome: Home) => {
            this.updateHome(patchedHome);
            resolve(patchedHome);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  deleteHome(home: Home): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.httpClient.delete(HomeService.homeUrl(home.id))
        .subscribe(
          _success => {
            this.homes.delete(home.id);
            resolve();
          },
          error => {
            reject(error);
          }
        );
    });
  }

  discoverDevices(homeID: number): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.httpClient.get(HomeService.discoverDevicesUrl(homeID))
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

  private setHomes(homes: Home[]) {
    if (this.homes === undefined) {
      this.homes = new Map<number, Home>();
    }

    this.homes.clear();
    for (const HOME of homes) {
      this.homes.set(HOME.id, HOME);
    }
  }

  private updateHome(newHome: Home) {
    this.homes.set(newHome.id, newHome);
  }
}
