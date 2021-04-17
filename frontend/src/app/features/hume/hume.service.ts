import { Observable } from 'rxjs';

import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';
import { EventService } from '../event/event.service';

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

  private homeHumeMap = new Map<number, Hume[]>()

  constructor(private httpService: HttpService,
              private eventService: EventService) { }

  getHomeHumes(homeID: number): Promise<Hume[]> {
    if (this.homeHumeMap.has(homeID)) {
      return Promise.resolve(this.homeHumeMap.get(homeID));
    }

    return new Promise<Hume[]>((resolve, reject) => {
      this.httpService.get(this.homeHumesUrl(homeID))
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

  humePaired(homeID: number, hume: Hume): void {
    this.addHomeHume(homeID, hume);
  }

  discoverDevices(humeUUID: string): Observable<any> {
    return this.httpService.get(this.discoverDevicesUrl(humeUUID));
  }

  private addHomeHume(homeID: number, hume: Hume) {
    this.homeHumeMap.get(homeID).push(hume);

    // Make sure the event service gets updates of all events for the added HUME.
    this.eventService.monitorHume(hume.uuid);
  }

  private replaceHomeHumes(homeID: number, humes: Hume[]): void {
    if (!this.homeHumeMap.has(homeID)) {
      this.homeHumeMap.set(homeID, [])
    }

    this.homeHumeMap.get(homeID).length = 0;
    for (const HUME of humes) {
      this.addHomeHume(homeID, HUME)
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
