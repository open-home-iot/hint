import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { EventService } from '../event/event.service';
import {Device} from '../device/device.service';

const HUME_URL = window.location.origin + '/api/humes/';

const HOME_URL = window.location.origin + '/api/homes/';

export class Hume {
  uuid: string;
  heartbeat: string;
  name: string;
  home: number;
}

@Injectable()
export class HumeService {

  private homeHumeMap = new Map<number, Hume[]>();
  private humeMap = new Map<string, Hume>();

  constructor(private httpClient: HttpClient,
              private eventService: EventService) { }

  getHomeHumes(homeID: number): Promise<Hume[]> {
    if (this.homeHumeMap.has(homeID)) {
      return Promise.resolve(this.homeHumeMap.get(homeID));
    }

    return new Promise<Hume[]>((resolve, reject) => {
      this.httpClient.get(this.homeHumesUrl(homeID))
        .subscribe(
          (humes: Hume[]) => {
            this.replaceHomeHumes(homeID, humes);
            resolve(this.homeHumeMap.get(homeID));
          },
          error => {
            reject(error);
          }
        );
    });
  }

  getHume(humeUUID: string): Hume {
    return this.humeMap.get(humeUUID);
  }

  attachDeviceUrl(homeID: number, device: Device) {
    return HOME_URL + String(homeID) + '/humes/' + device.hume + '/devices/' +
      device.address + '/attach';
  }

  attach(humeUuid: string, device: Device) {
    const HUME = this.humeMap.get(humeUuid);

    this.httpClient.post(this.attachDeviceUrl(HUME.home, device), {})
      .subscribe(
        ok => {},
        error => {
          console.error(error);
        }
      );
  }

  findHume(uuid: string): Promise<Hume> {
    return new Promise<Hume>((resolve, reject) => {
      this.httpClient.get(HUME_URL + uuid)
        .subscribe(
          (hume: Hume) => {
            resolve(hume);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  pairHume(homeId: number, hume: Hume) {
    this.httpClient.post(this.humePairUrl(hume.uuid),
                   {home_id: homeId})
      .subscribe(
        () => {
          this.humePaired(homeId, hume);
        },
        error => {
          console.error(error);
        }
      );
  }

  humePaired(homeID: number, hume: Hume): void {
    this.addHomeHume(homeID, hume);
  }

  discoverDevices(homeID: number, humeUUID: string): Observable<any> {
    return this.httpClient.get(this.discoverDevicesUrl(homeID, humeUUID));
  }

  private replaceHomeHumes(homeID: number, humes: Hume[]): void {
    if (!this.homeHumeMap.has(homeID)) {
      this.homeHumeMap.set(homeID, []);
    }

    this.homeHumeMap.get(homeID).length = 0;
    for (const HUME of humes) {
      this.addHomeHume(homeID, HUME);
    }
  }

  private addHomeHume(homeID: number, hume: Hume) {
    this.homeHumeMap.get(homeID).push(hume);
    this.humeMap.set(hume.uuid, hume);

    // Make sure the event service gets updates of all events for the added HUME.
    this.eventService.monitorHume(hume.uuid);
  }

  private homeHumesUrl(homeId: number): string {
    return HOME_URL + String(homeId) + '/humes';
  }

  private humePairUrl(humeUuid: string): string {
    return HUME_URL + humeUuid + '/confirm-pairing';
  }

  private discoverDevicesUrl(homeID: number, humeUUID: string) {
    return HOME_URL + String(homeID) +
      '/humes/' + humeUUID + '/devices/discover';
  }
}
