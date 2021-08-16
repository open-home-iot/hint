import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { EventService } from '../event/event.service';
import {Device} from '../device/device.service';

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

  private homeHumeMap = new Map<number, Hume[]>();

  constructor(private httpClient: HttpClient,
              private eventService: EventService) { }

  attachDeviceUrl(humeUuid: string, device: Device) {
    return HUME_URL + humeUuid + '/devices/' + device.address + '/attach';
  }

  attach(humeUuid: string, device: Device) {
    this.httpClient.post(this.attachDeviceUrl(humeUuid, device), {})
      .subscribe(
        ok => {},
        error => {
          console.error(error);
        }
      );
  }

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

  discoverDevices(humeUUID: string): Observable<any> {
    return this.httpClient.get(this.discoverDevicesUrl(humeUUID));
  }

  private addHomeHume(homeID: number, hume: Hume) {
    this.homeHumeMap.get(homeID).push(hume);

    // Make sure the event service gets updates of all events for the added HUME.
    this.eventService.monitorHume(hume.uuid);
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
