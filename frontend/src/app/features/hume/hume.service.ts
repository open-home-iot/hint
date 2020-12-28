import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';

import { Device } from '../device/device.service';


const HUME_URL = window.location.origin + "/api/humes/";

const HOME_URL = window.location.origin + "/api/homes/";

export class Hume {
  uuid: string;
  name: string;
  heartbeat: string;
  home: string;
}

@Injectable()
export class HumeService {

  private humes: { [homeId: number]: Hume[]  } = {};

  constructor(private httpService: HttpService) {
    console.log("Constructing HumeService");
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

  private pushHume(hume: Hume, homeId: number) {
    console.log("Adding HUME: " + hume.uuid + " to homeId: " + homeId);
    if (homeId in this.humes) {
      this.humes[homeId].push(hume);
    } else {
      this.humes[homeId] = [hume];
    }
  }

  private homeHumesUrl(homeId: number): string {
    return HOME_URL + String(homeId) + "/humes";
  }

  initHomeHumes(homeId: number): Hume[] {
    console.log("Getting humes for home: " + String(homeId))
    if (homeId in this.humes) {
      console.log("Home id already has an entry in Home->Humes map")
      return this.humes[homeId];
    } else {
      this.humes[homeId] = [];

      let obs = this.httpService.get(this.homeHumesUrl(homeId));
      obs.subscribe(
        (humes: Hume[]) => {
          console.log(humes);
          for (let hume of humes) {
            this.pushHume(hume, homeId);
          }
        },
        error => {
          console.log("Get HOME HUMEs failed.");
        }
      );

      return this.humes[homeId];
    }
  }

  private humePairUrl(humeUuid: string): string {
    return HUME_URL + humeUuid + "/confirm-pairing";
  }

  pairHume(homeId: number, hume: Hume) {
    this.httpService.post(this.humePairUrl(hume.uuid),
                          {"home_id": homeId})
      .subscribe(
        () => {
          this.humePaired(homeId, hume);
        },
        () => {
          console.log("HUME pairing failed.")
        }
      );
  }

  humePaired(homeId: number, hume: Hume) {
    this.humes[homeId].push(hume);
  }

  private discoverDevicesUrl(humeUUID: string) {
    return HUME_URL + humeUUID + "/devices/discover";
  }

  discoverDevices(humeUUID: string) {
    return this.httpService.get(this.discoverDevicesUrl(humeUUID));
  }
}
