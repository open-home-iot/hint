import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';

import { Device } from '../device/device.service';


const HUME_URL = window.location.origin + '/api/humes/';

const HOME_URL = window.location.origin + '/api/homes/';

export class Hume {
  uuid: string;
  name: string;
  heartbeat: string;
  home: string;
}

@Injectable()
export class HumeService {

  private humes: { [homeId: number]: Hume[]  } = {};

  constructor(private httpService: HttpService) { }

  getHomeHumes(homeId: number) {
    if (homeId in this.humes) {
      return this.humes[homeId];
    } else {
      this.humes[homeId] = [];
      return this.humes[homeId];
    }
  }

  findHume(uuid: string) {
    return new Promise((resolve, reject) => {
      this.httpService.get(HUME_URL + uuid)
        .subscribe(
          (hume: Hume) => {
            resolve(hume);
          },
          error => {
            reject();
          }
        );
    });
  }

  initHomeHumes(homeId: number): Hume[] {
    if (homeId in this.humes) {
      return this.humes[homeId];
    } else {
      this.humes[homeId] = [];

      const OBS = this.httpService.get(this.homeHumesUrl(homeId));
      OBS.subscribe(
        (humes: Hume[]) => {
          for (const HUME of humes) {
            this.pushHume(HUME, homeId);
          }
        },
        error => {
          console.error('Get HOME HUMEs failed: ', error);
        }
      );

      return this.humes[homeId];
    }
  }

  pairHume(homeId: number, hume: Hume) {
    this.httpService.post(this.humePairUrl(hume.uuid),
                          {home_id: homeId})
      .subscribe(
        () => {
          this.humePaired(homeId, hume);
        },
        () => {
          console.log('HUME pairing failed.');
        }
      );
  }

  humePaired(homeId: number, hume: Hume) {
    this.humes[homeId].push(hume);
  }

  discoverDevices(humeUUID: string) {
    return this.httpService.get(this.discoverDevicesUrl(humeUUID));
  }

  private pushHume(hume: Hume, homeId: number) {
    if (homeId in this.humes) {
      this.humes[homeId].push(hume);
    } else {
      this.humes[homeId] = [hume];
    }
  }

  private homeHumesUrl(homeId: number): string {
    return HOME_URL + String(homeId) + '/humes';
  }

  private humePairUrl(humeUuid: string): string {
    return HUME_URL + humeUuid + '/confirm-pairing';
  }

  private discoverDevicesUrl(humeUUID: string) {
    return HUME_URL + humeUUID + '/devices/discover';
  }
}
