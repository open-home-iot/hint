import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

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

  private static homeHumesUrl(homeId: number): string {
    return HOME_URL + String(homeId) + '/humes';
  }

  private static humePairUrl(humeUuid: string): string {
    return HUME_URL + humeUuid + '/confirm-pairing';
  }

  private static humeUrl(humeUuid: string): string {
    return HUME_URL + humeUuid;
  }

  getHomeHumes(homeID: number): Promise<Hume[]> {
    if (this.homeHumeMap.has(homeID)) {
      return Promise.resolve(this.homeHumeMap.get(homeID));
    }

    return new Promise<Hume[]>((resolve, reject) => {
      this.httpClient.get(HumeService.homeHumesUrl(homeID))
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
        _ok => {},
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

  pairHume(homeId: number, hume: Hume): Promise<Hume> {
    return new Promise<Hume>((resolve, reject) => {
      this.httpClient.post(HumeService.humePairUrl(hume.uuid),{home_id: homeId})
        .subscribe(
          () => {
            resolve(hume);
            this.humePaired(homeId, hume);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  changeName(hume: Hume, newName: string): Promise<Hume> {
    return new Promise<Hume>((resolve, reject) => {
      this.httpClient.patch(HumeService.humeUrl(hume.uuid), {name: newName})
        .subscribe(
          (updatedHume: Hume) => {
            // update the name in the humeMap, same object reference exists
            // in homeHumeMap so name will be updated in both places.
            let existingHume = this.humeMap.get(hume.uuid);
            existingHume.name = updatedHume.name;
          },
          error => {
            reject(error);
          }
        );
    });
  }

  deleteHume(hume: Hume): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.httpClient.delete(HumeService.humeUrl(hume.uuid))
        .subscribe(
          _success => {
            this.clearHume(hume);
            resolve();
          },
          error => {
            reject(error);
          }
        );
    });
  }

  private humePaired(homeID: number, hume: Hume): void {
    this.addHomeHume(homeID, hume);
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

  private clearHume(hume: Hume) {
    this.humeMap.delete(hume.uuid);

    let humes = this.homeHumeMap.get(hume.home);

    const INDEX = humes.indexOf(hume);
    const DELETED_ITEMS = humes.splice(INDEX, 1);

    if (DELETED_ITEMS.length !== 1) {
      console.error('failed to delete the hume from the array');
    }
  }
}
